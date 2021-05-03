import { HttpClient, HttpParams } from "@angular/common/http";
import { Component, HostListener, OnInit } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";
import { map } from "rxjs/operators";
import { environment } from "src/environments/environment";
import { IMetaData } from "../metaData/meta-data.component";

interface DatamartDef {
  identifier: string;  
  metadataId: string;
  hnr: string;
}

@Component({
  selector: "app-datamart-creation",
  templateUrl: "./datamart-creation.component.html",
  styleUrls: ["./datamart-creation.component.scss"]
})
export class DatamartCreationComponent implements OnInit {

  private readonly STATE_NAME = 'datamartCreationPageState';

  public readonly targetStorageSystems = [
    { system: 'MongoDB' },
    { system: 'PostgreSQL' },
    { system: 'CSV' },
    { system: 'XML' },
    { system: 'JSON' },
  ]

  public readonly joinMethods = [
    { method: 'inner' },
    { method: 'outer' },
    { method: 'leftouter' },
    { method: 'rightouter' },
    { method: 'leftsemi' },
    { method: 'leftanti' },
    { method: 'cross' },
  ]
  
  private session: string;

  //----- selection -------------------------------------------------------------------------------
  public isSearching = false
  public searchString$ = new BehaviorSubject<string>("");
  public searchResults$ = new BehaviorSubject<IMetaData[]>([]);
  public selectedMarts$ = new BehaviorSubject<DatamartDef[]>([]);

  
  //----- pyspark ---------------------------------------------------------------------------------
  public pyspark: string;

  //----- query -----------------------------------------------------------------------------------
  public query: string;

  //----- preview ---------------------------------------------------------------------------------
  public previewSchema: any;
  public previewRows: any;
  public previewError: string;
  public isGeneratingPreview = false;
  public isPollingPreview = false;
  public previewRowCount  = 10;

  //----- save ------------------------------------------------------------------------------------
  public humanReadableName: string;
  public comment: string;
  public targetStorageSystem: string;
  public csvHasHeader: boolean;
  public csvDelimiter: string;
  public xmlRowTag: string;
  public endDialogVisible = false;

  constructor(private httpClient: HttpClient) {}

  //-----------------------------------------------------------------------------------------------
  //----- public methods
  //-----------------------------------------------------------------------------------------------

  //----- component -------------------------------------------------------------------------------
  public async ngOnInit() {
    this.loadSession();
    this.loadState();
    this.searchString$.subscribe(() => 
      this.search()
    );
  }

  @HostListener('window:beforeunload', ['$event']) unloadHandler(event: Event) {
    this.saveState();
  }

  //----- selection -------------------------------------------------------------------------------
  public search() {
    let keyword = this.searchString$.value;
    let params;
    if (keyword && keyword !== '') {
      params = new HttpParams().append('search', keyword);
    }
    this.isSearching = true;
    this.httpClient.get<{ metaDatas: IMetaData[]}>(
      `${environment.backendUrl}/metaData`,
      {
        withCredentials: true,
        observe: 'response',
        params
      }
    ).subscribe(r => {
      const notSelectedResults:  IMetaData[] = [];
      r.body.metaDatas.forEach(metadata => {
        const index = this.selectedMarts$.value.findIndex(
          ({metadataId}) => metadataId === metadata.uid
        )
        if (index === -1) {
          notSelectedResults.push(metadata)
        }
      })

      this.searchResults$.next(notSelectedResults);
      this.isSearching = false;
    });
  }

  public selectDatamart(index: number) {
    let selected = this.selectedMarts$.value;
    let searchResults = this.searchResults$.value;
    selected.push({
      identifier: "",
      metadataId: searchResults[index].uid,
      hnr: searchResults[index].humanReadableName
    });
    searchResults.splice(index, 1);
    this.searchResults$.next(searchResults);
    this.selectedMarts$.next(selected);
  }

  public unselectDatamart(index: number) {
    let selected = this.selectedMarts$.value;
    selected.splice(index, 1);
    this.selectedMarts$.next(selected);
    this.search();
  }

  //----- preview ---------------------------------------------------------------------------------
  public generatePreview() {
    this.isGeneratingPreview = true
    this.previewError = null;
    const datamarts = {}
    this.selectedMarts$.value.forEach(datamart => {
      datamarts[datamart.identifier] = datamart.metadataId
    });
    const body = {
      session: this.session,
      datamarts,
      query: this.query,
      pyspark: this.pyspark
    }
    this.httpClient.post(`${environment.backendUrl}/datamarts/preview`, body, {
      withCredentials: true,
      observe: 'response'
    }).subscribe(
      ({ status }) => {
        if (status === 200 || status === 202) {
          this.pollPreview()
        }
      },
      (error) => {
        this.isGeneratingPreview = false
      },
      () => {}
    )
  }

  //----- save ------------------------------------------------------------------------------------
  public save() {
    this.httpClient.post<string>(
      `${environment.backendUrl}/datamarts/save`,
      {
        session: this.session,
        datamarts: this.selectedMarts$.value.map(e => e.metadataId),
        humanReadableName: this.humanReadableName,
        comment: this.comment,
        targetStorageSystem: this.targetStorageSystem,
        xmlRowTag: this.xmlRowTag,
        csvDelimiter: this.csvDelimiter,
        csvHasHeader: this.csvHasHeader
      },
      { withCredentials: true }
    ).subscribe(response => {
      this.endDialogVisible = true;
    })
  }

  //-----------------------------------------------------------------------------------------------
  //----- private methods 
  //-----------------------------------------------------------------------------------------------

  //----- component -------------------------------------------------------------------------------
  private saveState() {
    const state = {
      query: this.query,
      selected: this.selectedMarts$.value,
      previewRowCount: this.previewRowCount,
      pyspark: this.pyspark
    };
    localStorage.setItem(this.STATE_NAME, JSON.stringify(state));
  }

  private loadState() {
    const state = JSON.parse(localStorage.getItem(this.STATE_NAME));
    if (!state) return;
    this.query = state.query;
    this.previewRowCount = state.previewRowCount ?? 10
    this.selectedMarts$.next(state.selected ?? [])
    this.pyspark = state.pyspark
  }
  
  //----- session ---------------------------------------------------------------------------------
  private loadSession() {
    if (!this.session) {
      let session = localStorage.getItem("datamartsSession");
      if (session) {
        this.session = session;
      } else {
        this.httpClient.get<string>(
          `${environment.backendUrl}/datamarts/session`, 
          { withCredentials: true }
        ).subscribe(response => {
          this.session = response
          localStorage.setItem("datamartsSession", response);
        })
      }
    }
  }

  //----- preview ---------------------------------------------------------------------------------
  private pollPreview() {
    if (this.isGeneratingPreview) {
      if (!this.isPollingPreview) {
        this.isPollingPreview = true;
        this.httpClient.get(`${environment.backendUrl}/datamarts/preview`, {
          withCredentials: true,
          observe: 'response',
          params: {
            "session": this.session,
            "previewRowCount": this.previewRowCount.toString()
          }
        }).subscribe(
          response => {
            this.isPollingPreview = false;
            
            if (response.status === 202) {
              setTimeout(() => this.pollPreview(), 1000)
            } else if (response.status === 201) {
              this.previewSchema = response.body['schema'];
              this.previewRows = response.body['rows'];
              this.previewError == null
              this.isGeneratingPreview = false;
            }
          },
          (error) => {
            this.previewSchema = null;
              this.previewRows = null;
            this.previewError = error.error.message
            this.isGeneratingPreview = false
            this.isPollingPreview = false;
          },
          () => {}
        )
      }
    } else {
      this.isPollingPreview = false;
    }
  }
}
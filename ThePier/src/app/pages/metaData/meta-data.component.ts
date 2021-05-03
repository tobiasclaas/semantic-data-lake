import { HttpClient, HttpParams } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { faChevronDown, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import { Store } from '@ngxs/store';
import * as moment from 'moment';
import { Moment } from 'moment';
import { BehaviorSubject } from 'rxjs';
import { ToggleMetadatPolling } from 'src/app/state/actions';
import { environment } from 'src/environments/environment';

export interface Ancestor {
  uid: string;
  heritage: Ancestor[];
}

export interface IMetaData {
  humanReadableName: string;
  schema: any;
  comment: string;
  uid: string;
  insertedAt: string;
  insertedBy: string;
  isDatabase: true;
  sourceConnection: string;
  sourceDBName: string;
  sourceCollectionOrTableName: string;
  csvDelimiter: string;
  csvHasHeader: false;

  mimetype: string;
  targetStorageSystem: string;
  targetURL: string;
  sourcePassword: string;
  sourceUser: string;
  expanded: boolean;
  heritage: Ancestor[]
}

@Component({
  selector: 'app-meta-data',
  templateUrl: './meta-data.component.html',
  styleUrls: ['./meta-data.component.scss'],
})
export class MetaDataComponent implements OnInit, OnDestroy {
  public readonly chevronDown = faChevronDown;
  public readonly chevronRight = faChevronRight;
  public readonly api = environment.backendUrl;
  Object = Object;
  JSON = JSON;

  public metaData$ = new BehaviorSubject<IMetaData[]>([]);
  public lastUpdated: Moment;
  public isFetching = false;

  private active = false;

  constructor(private httpClient: HttpClient, private store: Store) {}

  public ngOnInit(): void {
    this.active = true;
    this.fetch();
  }

  public ngOnDestroy() {
    this.active = false;
  }

  public fetch() {
    if (this.active && !this.isFetching) {
      this.isFetching = true;
      this.httpClient
        .get<{ metaDatas: IMetaData[] }>(environment.backendUrl + '/metaData', {
          withCredentials: true,
          observe: 'response',
        })
        .subscribe((response) => {
          if (response.status === 200) {
            this.metaData$.next(response.body.metaDatas);
            this.lastUpdated = moment();
          }
          this.isFetching = false;
        });
    }
  }

  public trackEntry(index: number, entry) {
    return entry.uid;
  }

  public search(keyword: string) {
    let params;
    if (keyword && keyword !== '') {
      params = new HttpParams().append('search', keyword);
    }
    this.isFetching = true;
    this.httpClient.get<{ metaDatas: IMetaData[]}>(
      `${environment.backendUrl}/metaData`,
      {
        withCredentials: true,
        observe: 'response',
        params
      }
    ).subscribe(r => {
      this.metaData$.next(r.body.metaDatas);
      this.isFetching = false;
    });
  }

  public saveChanges(metadata) {
    if (confirm(`overwrite metadata for ${metadata.humanReadableName ?? metadata.uid}?`)) {
      this.isFetching = true;
      this.httpClient.put(
        `${environment.backendUrl}/metaData/${metadata.uid}`,
        {
          comment: metadata.comment,
          annotatedSchema: metadata.schema,
          humanReadableName: metadata.humanReadableName
        },
        {
          withCredentials: true,
          observe: 'response',
        }
      )
      .subscribe((response) => {
        this.isFetching = false;
        const updatedMetadata = response.body['metaData'];
        const i = metadata.findIndex((m) => m.uid === updatedMetadata.uid);
        metadata[i] = updatedMetadata;
        this.metaData$.next(metadata);
      });
    }
  }

  public revertChanges(metadata: IMetaData) {
    this.isFetching = true;
    this.httpClient
      .get(`${environment.backendUrl}/metaData/${metadata.uid}`, {
        withCredentials: true,
        observe: 'response',
      })
      .subscribe((response) => {
        const originalMetadata = response.body['metaData'] as IMetaData;
        const allMetadata = this.metaData$.value;
        const i = allMetadata.findIndex((m) => m.uid === originalMetadata.uid);
        originalMetadata.expanded = metadata.expanded;
        allMetadata[i] = originalMetadata;
        this.metaData$.next(allMetadata);
        this.isFetching = false;
      });
  }

  public delete(metadata: IMetaData) {
    if (confirm(`Delete DataMart ${metadata.humanReadableName ?? metadata.uid}?`)) {
      this.httpClient.delete(
        `${environment.backendUrl}/metaData/${metadata.uid}`,
        {
          withCredentials: true,
          observe: 'response'
        }
      ).subscribe(r => {
        this.fetch();
      });
    }
  }

  public hnrInputClick(event) {
    event.preventDefault();
    return false;
  }
}

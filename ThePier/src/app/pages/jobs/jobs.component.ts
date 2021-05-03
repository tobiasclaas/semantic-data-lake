import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, HostListener, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { faExclamationCircle, faCheckCircle, faClock } from '@fortawesome/free-solid-svg-icons';
import { Store } from '@ngxs/store';
import * as moment from 'moment';
import { Moment } from 'moment';
import { BehaviorSubject } from 'rxjs';
import { DeleteJob, SetJobPageState, ToggleJobsPolling, UpdateJobsList } from 'src/app/state/actions';
import { IAPIJob, IJob, JobStates } from 'src/app/state/objects';
import { PersistentState } from 'src/app/state/persistent.state';
import { VolatileState } from 'src/app/state/volatile.state';
import { environment } from 'src/environments/environment';
import { IngestionComponent } from './components/ingest/ingestion.component';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss'],
})
export class JobsComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('ingestionComponent') private ingestComponent: IngestionComponent;

  public jobs$ = new BehaviorSubject<IJob[]>([]);
  public lastUpdated: Moment;
  public pollInfo: {
    poll: boolean;
    intervall: number;
  };
  public isFetching = false;

  public ingestionVisible = false;

  private active = false;

  constructor(private store: Store, private router: Router, private httpClient: HttpClient) {
    store.select(VolatileState.jobs).subscribe(({ jobs, jobsLastUpdated }) => {
      this.jobs$.next(jobs);
      this.lastUpdated = jobsLastUpdated;
    });
    store.select(PersistentState.jobs).subscribe(({ pollJobs, jobsPollingInterval }) => {
      this.pollInfo = {
        poll: pollJobs,
        intervall: jobsPollingInterval,
      };
      if (pollJobs) {
        this.fetch();
      }
    });
  }

  @HostListener('window:beforeunload', ['$event']) unloadHandler(event: Event) {
    this.persistState();
  }

  public ngOnInit(): void {
    this.active = true;
    this.restoreState();
    this.fetch();
  }

  public ngAfterViewInit(): void {
  }

  public ngOnDestroy(): void {
    this.active = false;
    this.persistState();
  }

  public ingest() {
    this.ingestionVisible = true;
  }

  public togglePolling() {
    this.store.dispatch(new ToggleJobsPolling());
  }

  public stateIcon(job: IJob) {
    switch (job.state) {
      case JobStates.succeeded:
        return faCheckCircle;
      case JobStates.failed:
        return faExclamationCircle;
      case JobStates.started:
        return faClock;
    }
  }

  public stateClass(job: IJob) {
    switch (job.state) {
      case JobStates.succeeded:
        return 'succeeded';
      case JobStates.failed:
        return 'failed';
      case JobStates.started:
        return 'running';
    }
  }

  public delete(uid: string) {
    if (confirm(`Delete job ${uid}?`)) {
      this.isFetching = true;
      this.httpClient.delete(
        `${environment.backendUrl}/job/${uid}`,
        {
          withCredentials: true,
          observe: 'response'
        }
      ).subscribe(r => {
        if (r.status === 204) {
          this.store.dispatch(new DeleteJob(uid));
        }
        this.isFetching = false;
      });
    }
  }

  private fetch() {
    if (this.active && !this.isFetching) {
      this.isFetching = true;
      this.httpClient
        .get<{ jobs: IAPIJob[] }>(environment.backendUrl + '/job', {
          withCredentials: true,
          observe: 'response',
        })
        .subscribe((response) => {
          if (response.status === 200) {
            const updatedJobs = response.body.jobs.map((apiJob) => this.mapApiJob(apiJob));
            this.store.dispatch(new UpdateJobsList(updatedJobs));
          }
          this.isFetching = false;

          if (this.pollInfo.poll) {
            setTimeout(() => this.fetch(), this.pollInfo.intervall);
          }
        });
    }
  }

  private mapApiJob(apiJob: IAPIJob): IJob {
    let state: JobStates;

    if (apiJob.endedAt == null) {
      state = JobStates.started;
    } else if (apiJob.failed) {
      state = JobStates.failed;
    } else {
      state = JobStates.succeeded;
    }

    const parsedStart = moment(apiJob.startedAt);
    const parsedEnd = apiJob.endedAt ? moment(apiJob.endedAt) : null;

    return {
      uid: apiJob.uid,
      startedBy: apiJob.startedBy,
      startedAt: parsedStart,
      state,
      errorMessage: apiJob.errorMessage,
      task: apiJob.task,
      endedAt: parsedEnd,
    };
  }

  private restoreState() {
    const state = this.store.selectSnapshot(PersistentState.jobPageState);
    this.ingestionVisible = state.ingestionVisible;
    if (this.ingestionVisible) {
      setTimeout(() =>  this.ingestComponent.restoreState(state.ingestion), 1);
    }
  }

  private persistState() {
    const state = {
      ingestionVisible: this.ingestionVisible,
      ingestion: this.ingestionVisible ? this.ingestComponent.persistState() : null,
    };
    this.store.dispatch(new SetJobPageState(state));
  }
}

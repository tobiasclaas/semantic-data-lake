import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { insertItem, patch, removeItem } from '@ngxs/store/operators';
import * as moment from 'moment';
import { Moment } from 'moment';
import { AddJob, DeleteJob, SetActiveUser, UpdateJobsList } from './actions';
import { IJob, IUser } from './objects';

export interface IVolatileState {
  activeUser: IUser;
  jobs: IJob[];
  jobsLastUpdated: Moment;
}

@Injectable({ providedIn: 'root' })
@State<IVolatileState>({
  name: 'volatile',
  defaults: {
    activeUser: null,
    jobs: [],
    jobsLastUpdated: null,
  },
})
export class VolatileState {
  //===== User ====================================================================================
  @Selector()
  static activeUser(state: IVolatileState) {
    return state.activeUser;
  }

  @Action(SetActiveUser)
  setActiveUser(ctx: StateContext<IVolatileState>, { payload }: SetActiveUser) {
    ctx.setState(
      patch<IVolatileState>({
        activeUser: payload,
      })
    );
  }

  //===== Jobs ====================================================================================
  @Selector()
  public static jobs(state: IVolatileState) {
    return {
      jobs: state.jobs,
      jobsLastUpdated: state.jobsLastUpdated,
    };
  }

  @Action(AddJob)
  private addJob(ctx: StateContext<IVolatileState>, { payload }: AddJob) {
    ctx.setState(
      patch<IVolatileState>({
        jobs: insertItem(payload),
        jobsLastUpdated: moment(),
      })
    );
  }

  @Action(UpdateJobsList)
  private updateJobsList(ctx: StateContext<IVolatileState>, { payload }: UpdateJobsList) {
    let updatedJobs: IJob[] = [];

    ctx.getState().jobs.forEach((job) => {
      let updatedJob = payload.findIndex(({ uid }) => uid === job.uid);
      if (updatedJob > -1) {
        updatedJobs.push(payload[updatedJob]);
        payload.splice(updatedJob, 1);
      } else {
        updatedJobs.push(job);
      }
    });

    updatedJobs = [...updatedJobs, ...payload];
    updatedJobs.sort(({ uid: a }, { uid: b }) => a.localeCompare(b));

    ctx.setState(
      patch<IVolatileState>({
        jobs: updatedJobs,
        jobsLastUpdated: moment(),
      })
    );
  }

  @Action(DeleteJob)
  private deleteJob(ctx: StateContext<IVolatileState>, { payload }: DeleteJob) {
    ctx.setState(
      patch<IVolatileState>({
        jobs: removeItem(({uid}) => uid === payload),
        jobsLastUpdated: moment(),
      })
    );
  }
}

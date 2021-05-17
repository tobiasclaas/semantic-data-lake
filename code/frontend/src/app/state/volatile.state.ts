import { Injectable } from '@angular/core';
import { Action, createSelector, Selector, State, StateContext } from '@ngxs/store';
import { insertItem, patch, removeItem } from '@ngxs/store/operators';
import * as moment from 'moment';
import { Moment } from 'moment';
import { AddJob, DeleteJob, SetActiveUser, SetDatamarts, UpdateJobsList } from './actions';
import { IDatamart, IJob, IUser } from './objects';

export interface IVolatileState {
    activeUser: IUser;
    jobs: IJob[];
    jobsLastUpdated: Moment;
    datamarts: Map<string, IDatamart>;
}

@Injectable({ providedIn: 'root' })
@State<IVolatileState>({
    name: 'volatile',
    defaults: {
        activeUser: null,
        jobs: [],
        jobsLastUpdated: null,
        datamarts: new Map()
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
                jobs: removeItem(({ uid }) => uid === payload),
                jobsLastUpdated: moment(),
            })
        );
    }

    //===== Datamarts ==============================================================================
    @Selector()
    static datamarts(state: IVolatileState) {
        return [... state.datamarts.values()];
    }

    static datamartsById(id: string) {
        return createSelector([VolatileState], (state: IVolatileState) => {
            return state.datamarts?.get(id)
        })
    }

    @Action(SetDatamarts)
    private setDatamarts(ctx: StateContext<IVolatileState>, { payload }: SetDatamarts) {
        let marts = new Map<string, IDatamart>()

        payload.forEach(p => {
            p.status.started = moment(p.status.started)
            p.status.ended = moment(p.status.ended)
            p.metadata.createdAt = moment(p.metadata.createdAt)
            marts.set(p.uid, p)
        })

        ctx.setState(
            patch<IVolatileState>({
                datamarts: marts
            })
        )
    }
}

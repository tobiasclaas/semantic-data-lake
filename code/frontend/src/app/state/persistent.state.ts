import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { patch } from '@ngxs/store/operators';
import {
    IPersistentHomeState,
    defaultPersistentHomeState,
} from '../pages/home/persisten-home.state';
import { SetJobPageState, ToggleJobsPolling, ToggleMetadatPolling, UpdatePersistentHomeState } from './actions';

export interface IPersistentState {
    pollJobs: boolean;
    jobsPollingInterval: number;
    pollMetadata: boolean;
    metadataPollingIntervall: number;
    jobPageState: any;
    homeState: IPersistentHomeState;
}

@Injectable({ providedIn: 'root' })
@State<IPersistentState>({
    name: 'persistent',
    defaults: {
        pollJobs: true,
        jobsPollingInterval: 5000,
        pollMetadata: true,
        metadataPollingIntervall: 5000,
        jobPageState: null,
        homeState: defaultPersistentHomeState,
    },
})
export class PersistentState {
    @Selector()
    public static jobs(state: IPersistentState) {
        return {
            pollJobs: state.pollJobs,
            jobsPollingInterval: state.jobsPollingInterval,
        };
    }

    @Selector()
    public static jobPageState(state: IPersistentState) {
        return state.jobPageState;
    }

    @Selector()
    public static metadata(state: IPersistentState) {
        return {
            pollMetadata: state.pollMetadata,
            metadataPollingIntervall: state.metadataPollingIntervall,
        };
    }

    @Action(ToggleJobsPolling)
    private toggleJobsPolling(ctx: StateContext<IPersistentState>) {
        ctx.setState(
            patch<IPersistentState>({ pollJobs: !ctx.getState().pollJobs })
        );
    }

    @Action(SetJobPageState)
    private setType(ctx: StateContext<IPersistentState>, { payload }: SetJobPageState) {
        ctx.setState(
            patch<IPersistentState>({
                jobPageState: payload,
            })
        );
    }

    @Action(ToggleMetadatPolling)
    private toggleMetadataPolling(ctx: StateContext<IPersistentState>) {
        ctx.setState(
            patch<IPersistentState>({ pollMetadata: !ctx.getState().pollMetadata })
        );
    }

    //===== Home ===================================================================================
    @Selector()
    public static homeState(state: IPersistentState) {
        return state.homeState;
    }

    @Action(UpdatePersistentHomeState)
    private updatePersistentHomeState(ctx: StateContext<IPersistentState>, { payload }: UpdatePersistentHomeState) {
        ctx.setState(
            patch<IPersistentState>({
                homeState: payload
            }) 
        )
    }
}

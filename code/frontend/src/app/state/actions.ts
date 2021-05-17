import { IPersistentHomeState } from '../pages/home/persisten-home.state';
import { IDatamart, IJob, IngestionType, IUser } from './objects';

//===== User ======================================================================================
export class SetActiveUser {
    static readonly type = '[ACTIVE USER] set';
    constructor(public payload: IUser) {}
}

//===== Jobs ======================================================================================
export class AddJob {
    public static readonly type = '[JOBS] Add';
    constructor(public payload: IJob) {}
}

export class DeleteJob {
    public static readonly type = '[JOBS] Delete';
    constructor(public payload: string) {}
}

export class UpdateJobsList {
    public static readonly type = '[JOBS] Update list';
    constructor(public payload: IJob[]) {}
}

export class ToggleJobsPolling {
    public static readonly type = '[JOBS] Toggle Polling';
}

export class SetJobPageState {
    static readonly type = '[JOB-PAGE] set pagestate';
    constructor(public payload: any | null) {}
}

//===== Metadata ==================================================================================
export class ToggleMetadatPolling {
    public static readonly type = '[Metadata] Toggle Polling';
}

//===== Datamarts ==================================================================================
export class SetDatamarts {
    public static readonly type = '[Datamarts] Set';
    constructor(public payload: IDatamart[]) {}
}

//===== Home =======================================================================================
export class UpdatePersistentHomeState {
    public static readonly type = '[HomeState] Update';
    constructor(public payload: IPersistentHomeState) {}
}
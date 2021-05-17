import { Moment } from 'moment';

//===== User =======================================================================================
export interface IUser {
    email: string;
    firstname: string;
    lastname: string;
    isAdmin: boolean;
}

//===== Jobs =======================================================================================
export interface IAPIJob {
    uid: string;
    task: string;
    startedBy: string;
    startedAt: string;
    endedAt: string;
    failed: boolean;
    errorMessage: string;
}

export enum JobStates {
    started,
    succeeded,
    failed,
}

export interface IJob {
    uid: string;
    startedBy: string;
    startedAt: Moment;
    state: JobStates;
    errorMessage?: string;
    task?: string;
    endedAt?: Moment;
}

//===== Ingestion ==================================================================================
export enum IngestionType {
    mongoDB,
    postgreSQL,
    file,
}

//===== DatamartStatus =============================================================================
export interface IDatamartStatus {
    state: string;
    started: Moment;
    ended: Moment;
    error: string;
}

//===== Metadata ===================================================================================
export interface IMetadata {
    createdAt: Moment;
    createdBy: IUser;
    heritage: IDatamart[];
    constructionCode: string;
    constructionQuery: string;
    source: {};
    target: {};
    schema: any;
}

//===== Datamart ===================================================================================
export interface IDatamart {
    uid: string;
    humanReadableName: string;
    comment: string;
    metadata: IMetadata;
    status: IDatamartStatus;
}
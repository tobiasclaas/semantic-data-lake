import { Moment } from 'moment';

//===== User ======================================================================================
export interface IUser {
  email: string;
  firstname: string;
  lastname: string;
  isAdmin: boolean;
}

//===== Jobs ======================================================================================
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

//===== Ingestion =================================================================================
export enum IngestionType {
  mongoDB,
  postgreSQL,
  file,
}

import { IDatamart } from "src/app/state/objects";

export interface IPersistentHomeState {
    detailsVisible: boolean;
    detialsDatamartId: string;
    ingestionVisible: boolean;
}

export const defaultPersistentHomeState: IPersistentHomeState = {
    detailsVisible: false,
    detialsDatamartId: null,
    ingestionVisible: false
}
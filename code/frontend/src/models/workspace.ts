import { IWithKey } from "./common";

export interface IWorkspaceExchange {
    name: string
}

export type IWorkspace = IWithKey<IWorkspaceExchange>

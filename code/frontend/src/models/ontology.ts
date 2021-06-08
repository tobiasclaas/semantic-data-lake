import { IWithKey } from "./common";

export interface IOntologyExchange {
  name: string;
}

export interface IOntologyPost extends IOntologyExchange {
  file: Blob;
}

export type IOntology = IWithKey<IOntologyExchange>;

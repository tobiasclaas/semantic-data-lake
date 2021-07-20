export type AutocompleteItemKeyValue = string | number;
export type AutocompleteItemGroupKeyValue = string | number | null;

export interface AutocompleteItem<
  T extends AutocompleteItemKeyValue,
  G extends AutocompleteItemGroupKeyValue | undefined = undefined
> {
  id: T;
  text: string;
  group: G;
}

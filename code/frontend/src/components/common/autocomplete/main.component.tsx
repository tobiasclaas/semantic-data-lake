import CircularProgress from "@material-ui/core/CircularProgress";
import { PopperProps } from "@material-ui/core/Popper";
import TextField, { TextFieldProps } from "@material-ui/core/TextField";
import Autocomplete, {
  AutocompleteChangeDetails,
  AutocompleteChangeReason,
} from "@material-ui/lab/Autocomplete";
import debounce from "lodash/debounce";
import React, { useRef } from "react";

import { AutocompleteItem } from "../../../models/autocomplete";

export interface AutocompleteComponentProps {
  title?: string;
  queryUrl: (term: string) => string;
  throttleDuration?: number;
  defaultValue?: AutocompleteItem;
  value?: AutocompleteItem | null;
  onChange?: (value: AutocompleteItem | null) => void;
  disabled?: boolean;
  popperComponent?: React.ComponentType<PopperProps>;
  textFieldProps?: TextFieldProps;
}

const defaultProps = {
  throttleDuration: 1500,
};

const AutocompleteComponent = (props: AutocompleteComponentProps) => {
  const [open, setOpen] = React.useState(false);
  const [options, setOptions] = React.useState<AutocompleteItem[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [text, setText] = React.useState("");
  const controllerRef = useRef<AbortController | null>();

  React.useEffect(() => {
    if (!open) {
      setOptions([]);
    }
  }, [open]);

  const search = async (term: string) => {
    if (controllerRef.current) {
      controllerRef.current.abort();
    }
    const controller = new AbortController();
    controllerRef.current = controller;

    try {
      setLoading(true);
      const res = await fetch(props.queryUrl(term), {
        signal: controllerRef.current?.signal,
        credentials: "include",
      });

      let items = (await res.json()) as AutocompleteItem[];

      setOptions(items);
      setLoading(false);
      controllerRef.current = null;
    } catch (e) {
      if (e.name !== "AbortError") {
        setLoading(false);
      }
    }
  };

  const delayedSearch = props.throttleDuration
    ? props.throttleDuration < 0
      ? search
      : debounce((term: string) => search(term), props.throttleDuration)
    : search;

  const inputChanged = (
    event: unknown,
    value: string,
    reason: string
  ): void => {
    setText(value);
    setOptions([]);

    if (!open || reason !== "input" || value.length < 3) return;

    delayedSearch(value);
  };
  return (
    <Autocomplete
      open={open}
      onOpen={() => {
        setOpen(true);
      }}
      onClose={() => {
        setOpen(false);
        if (controllerRef.current) {
          controllerRef.current.abort();
          controllerRef.current = null;
        }
        setLoading(false);
      }}
      PopperComponent={props.popperComponent}
      getOptionSelected={(option, value) => option.value === value.value}
      getOptionLabel={(option) => option.text}
      filterOptions={(options, state) => options}
      options={options}
      onInputChange={inputChanged}
      loading={loading}
      disabled={props.disabled}
      value={props.value}
      inputValue={text}
      onChange={(
        event: React.ChangeEvent<unknown>,
        value: AutocompleteItem | null,
        reason: AutocompleteChangeReason,
        details?: AutocompleteChangeDetails<AutocompleteItem> | undefined
      ) => {
        if (props.onChange) props.onChange(value);
      }}
      defaultValue={props.defaultValue}
      renderInput={(params) => (
        <TextField
          {...params}
          label={props.title}
          required
          {...props.textFieldProps}
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <React.Fragment>
                {loading ? (
                  <CircularProgress color="inherit" size={20} />
                ) : null}
                {params.InputProps.endAdornment}
              </React.Fragment>
            ),
            ...props.textFieldProps?.InputProps,
          }}
        />
      )}
    />
  );
};

AutocompleteComponent.defaultProps = defaultProps;

export default AutocompleteComponent;

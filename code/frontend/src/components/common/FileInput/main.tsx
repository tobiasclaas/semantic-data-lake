import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import IconButton from "@material-ui/core/IconButton";
import PublishIcon from "@material-ui/icons/Publish";
import TextField from "@material-ui/core/TextField";
import CloseIcon from "@material-ui/icons/Close";

export interface FileInputProps {
  label?: string;
  onChange?: (value: File | null) => void;
  accept?: string;
}

const FileInput: React.FC<FileInputProps> = (props) => {
  const { t } = useTranslation();
  const [filename, setFilename] = useState<string>("");
  const onChangeHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length == 1) {
      const file = e.target.files[0];
      setFilename(file.name);
      if (props.onChange) props.onChange(file);
    }
  };

  return (
    <TextField
      margin="dense"
      fullWidth
      label={props.label}
      value={filename}
      placeholder={t("generic.browse")}
      InputProps={{
        readOnly: true,
        endAdornment: (
          <IconButton
            edge="end"
            size="small"
            component="label"
            onClick={(event: any) => {
              if (filename) {
                event.preventDefault();
                setFilename("");
                if (props.onChange) props.onChange(null);
              }
            }}
          >
            {filename.length > 0 ? (
              <CloseIcon fontSize="small" />
            ) : (
              <PublishIcon fontSize="small" />
            )}

            {filename.length > 0 ? null : (
              <input
                type="file"
                accept={props.accept}
                onChange={onChangeHandler}
                hidden
              />
            )}
          </IconButton>
        ),
      }}
    ></TextField>
  );
};

export default FileInput;

import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import FileInput from "../../../../common/FileInput";
import Grid from "@material-ui/core/Grid";
import { TextField } from "@material-ui/core";
import Checkbox from "@material-ui/core/Checkbox";
import FormControlLabel from "@material-ui/core/FormControlLabel";

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <Grid item container xs>
        <FileInput
          label={t("generic.file")}
          accept=".json"
          onChange={(v) => viewModel.setFile(v)}
        />
      </Grid>
      <Grid container spacing={2} item style={{ alignItems: "center" }}>
        <Grid item sm>
          <TextField
            fullWidth
            autoFocus
            onChange={(e) => viewModel.setDelimiter(e.target.value)}
            value={viewModel.delimiter}
            margin="dense"
            label={t("dataset_management.upload.csv.delimiter")}
          />
        </Grid>
        <Grid item sm>
          <FormControlLabel
            control={
              <Checkbox
                checked={viewModel.hasHeader}
                color="primary"
                onChange={(e) => viewModel.setHasHeader(e.target.checked)}
              />
            }
            label={t("dataset_management.upload.csv.has_header")}
          />
        </Grid>
      </Grid>
    </React.Fragment>
  );
});

export default Main;

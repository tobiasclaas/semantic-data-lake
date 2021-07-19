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
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';



const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();



  return (
      /**
       *  Return @Params
       *  Distinct file selection csv
       *  Check parameter Delimiter, HasHeader, Comment, Target Storage.
       *
       */
    <React.Fragment>
      <Grid item container xs>
        <FileInput
        required
          label={t("generic.file")}
          accept=".csv"
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
        <Grid item>
          <FormControlLabel
            control={
              <TextField
              fullWidth
              autoFocus
              onChange={(e) => viewModel.setComment(e.target.value)}
              value={viewModel.comment}
              margin="dense"
              label={t("dataset_management.upload.csv.comment")}
            />
            }
          />
        </Grid>
        <Grid item>
          <FormControlLabel
            control={
              <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={viewModel.target_storage}
              onChange={(e) => viewModel.setTargetStorage(e.target.value)}
            >
              <MenuItem value={"HDFS"}>HDFS</MenuItem>
              <MenuItem value={"MongoDB"}>MongoDB</MenuItem>
              label={t("dataset_management.upload.csv.target_storage")}
            </Select>
            }
          />
        </Grid>
      </Grid>
    </React.Fragment>
  );
});

export default Main;

/**
 * Export Params to csv/viewModel
 */



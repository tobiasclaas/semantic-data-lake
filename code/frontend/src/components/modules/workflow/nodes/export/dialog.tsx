import React, { useRef, useState } from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import TextField from "@material-ui/core/TextField";
import IViewProps from "../../../../../models/iViewProps";
import Grid from "@material-ui/core/Grid";
import MenuItem from "@material-ui/core/MenuItem";
import InputLabel from "@material-ui/core/InputLabel";
import { useTranslation } from "react-i18next";
import Select from "@material-ui/core/Select";
import FormControl from "@material-ui/core/FormControl";

const Dialog: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();
  return (
    <Grid container direction="column">
      <Grid item sm>
        <FormControl fullWidth margin="dense">
          <TextField
            label={t("workflow.properties_dialog.export.name")}
            value={viewModel.data?.name ?? ""}
            onChange={(e) =>
              viewModel.updateData((d) => (d.name = e.target.value))
            }
          />
        </FormControl>
      </Grid>
      <Grid item sm>
        <FormControl fullWidth margin="dense">
          <InputLabel>
            {t("workflow.properties_dialog.export.target")}
          </InputLabel>
          <Select
            value={viewModel.data?.target ?? ""}
            onChange={(e) =>
              viewModel.updateData(
                (data) => (data.target = e.target.value as string)
              )
            }
          >
            <MenuItem value="HDFS">HDFS</MenuItem>
            <MenuItem value="MongoDB">MongoDB</MenuItem>
          </Select>
        </FormControl>
      </Grid>
    </Grid>
  );
});

export default Dialog;

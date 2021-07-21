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

const Dialog: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) =>
    /**
     *
     * @param viewModel
     */
{
  const { t } = useTranslation();
  return (
      /**
       *  @return
       * @param select viewModel
       */
    <Grid container direction="column">
      <Grid item sm>
        <FormControl fullWidth margin="dense">
          <InputLabel>
            {t("workflow.properties_dialog.join.column", { name: 1 })}
          </InputLabel>
          <Select
            value={viewModel.data.field.input_1 ?? ""}
            onChange={(e) =>
              viewModel.updateData((data) => {
                data.field.input_1 = e.target.value as string;
                data.schema.fields = [
                  ...viewModel.firstInputFields,
                  ...viewModel.secondInputFields,
                ];
              })
            }
          >
            {viewModel.firstInputFields.map((item, index) => (
              <MenuItem value={item.name} key={index}>
                {item.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid item sm>
        <FormControl fullWidth margin="dense">
          <InputLabel>
            {t("workflow.properties_dialog.join.column", { name: 2 })}
          </InputLabel>
          <Select
            value={viewModel.data.field.input_2 ?? ""}
            onChange={(e) =>
              viewModel.updateData((data) => {
                data.field.input_2 = e.target.value as string;
                data.schema.fields = [
                  ...viewModel.firstInputFields,
                  ...viewModel.secondInputFields,
                ];
              })
            }
          >
            {viewModel.secondInputFields.map((item, index) => (
              <MenuItem value={item.name} key={index}>
                {item.name}
              </MenuItem>
            ))}{" "}
          </Select>
        </FormControl>
      </Grid>
    </Grid>
  );
});

export default Dialog;

import React, { useRef, useState } from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import TextField from "@material-ui/core/TextField";
import IViewProps from "../../../../../models/iViewProps";
import Grid from "@material-ui/core/Grid";
import { useTranslation } from "react-i18next";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import Paper from "@material-ui/core/Paper";
import Chip from "@material-ui/core/Chip";
import { makeStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles";
import { createStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme: Theme) =>
    /**
     *
     * @param theme
     */
  createStyles({
    chipContainer: {
      display: "flex",
      justifyContent: "center",
      flexWrap: "wrap",
      listStyle: "none",
      padding: theme.spacing(0.5),
      margin: 0,
    },
    chip: {
      margin: theme.spacing(0.5),
    },
  })
);

const Dialog: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) =>
    /**
     *
     * @param viewModel
     */
{
  const { t } = useTranslation();
  const classes = useStyles();

  return (
      /**
       * @return
       * @param group column
       */
    <Grid container direction="column">
      <Grid item sm>
        <FormControl fullWidth margin="dense">
          <InputLabel>
            {t("workflow.properties_dialog.groupby.column")}
          </InputLabel>
          <Select
            value={
                viewModel.data.group_by
            }
            onChange={(e) =>
              viewModel.updateData((data) => {
                  data.group_by = e.target.value as string;
                // data.schema.fields.push(
                //   viewModel.currentFields[e.target.value as number]
                // );
              })
            }
          >
            {viewModel.currentFields.map((item, index) => (
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
                    {t("workflow.properties_dialog.groupby.select")}
                </InputLabel>
                <Select
                    value={
                        viewModel.data.aggregate_select
                    }
                    onChange={(e) =>
                        viewModel.updateData((data) => {
                            data.aggregate_select = e.target.value as string;
                        })
                    }
                >
                    {viewModel.currentFields.filter(item => item.type == "integer").map((item, index) => (
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
                    {t("workflow.properties_dialog.groupby.function")}
                </InputLabel>
                <Select
                    value={viewModel.data.aggregate_function}
                    onChange={(e) =>
                        viewModel.updateData((data) => {
                            data.aggregate_function = e.target.value as string;
                        })
                    }
                >
                <MenuItem value="count" key="count">
                    Count
                </MenuItem>
                <MenuItem value="avg" key="avg">
                    Average
                </MenuItem>
                <MenuItem value="sum" key="sum">
                    Sum
                </MenuItem>
                <MenuItem value="min" key="min">
                    Min
                </MenuItem>
                <MenuItem value="max" key="max">
                    Max
                </MenuItem>

                </Select>
            </FormControl>
        </Grid>
    </Grid>
  );
});

export default Dialog;

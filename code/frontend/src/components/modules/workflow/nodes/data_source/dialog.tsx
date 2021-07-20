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
       * @return
       */
      <Grid container direction="column">
        <Grid container item>
          <Grid item sm>
            <FormControl fullWidth margin="dense">
              <InputLabel>
                {t("workflow.properties_dialog.data_source.datamart")}
              </InputLabel>
              <Select
                value={viewModel.data?.uid ?? ""}
                onChange={(e) =>
                  viewModel.updateData((data) => {
                    const uid = e.target.value as string;
                    data.uid = uid;
                    const datamart = viewModel.workflowViewModel.datamarts.find(
                      (i) => i.uid == uid
                    );
                    data.schema.fields = (
                      datamart as any
                    ).metadata.schema.fields;

                    viewModel.workflowViewModel.annotations.forEach((i) => {
                      if (i.datamart_id != uid) return;
                      if (
                        i.ontology_attribute.find(
                          (x) =>
                            x[1] ==
                            "<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C49189>"
                        )
                      )
                        data.schema.primary_key.push(i.data_attribute);
                    });
                    console.log(data.schema.primary_key);
                  })
                }
              >
                {viewModel.workflowViewModel.datamarts.map((i) => (
                  <MenuItem value={i.uid} key={i.uid}>
                    {i.humanReadableName}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Grid>
    );
  }
);

export default Dialog;

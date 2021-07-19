import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import { TreeItem, TreeView } from "@material-ui/lab";
import { Field, isArray, isStruct } from "../../../../models/datamarts";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";

const Main: React.FC<{ field: Field; path: string; viewModel: ViewModel }> =
  observer(({ field, path, viewModel }) => {
    const { t } = useTranslation();

    let type = field.type;
    while (isArray(type)) {
      type = type.elementType;
    }

    return (
      <Grid container direction="column">
        <Grid item container xs spacing={1} alignItems="center">
          <Grid item>
            <Typography variant="overline">{`${t(
              "generic.path"
            )}:`}</Typography>
          </Grid>
          <Grid item>
            <Typography variant="overline" style={{ textTransform: "none" }}>
              {path}
            </Typography>
          </Grid>
        </Grid>

        <Grid item container xs spacing={1} alignItems="center">
          <Grid item>
            <Typography variant="overline">{`${t(
              "generic.nullable"
            )}:`}</Typography>
          </Grid>
          <Grid item>
            <Typography variant="overline" style={{ textTransform: "none" }}>
              {field.nullable ? t("generic.yes") : t("generic.no")}
            </Typography>
          </Grid>
        </Grid>

        <Grid item container xs spacing={1} alignItems="center">
          <Grid item>
            <Typography variant="overline">{`${
              isArray(field.type) ? t("generic.item_type") : t("generic.type")
            }:`}</Typography>
          </Grid>
          <Grid item>
            <Typography variant="overline" style={{ textTransform: "none" }}>
              {isStruct(type) ? type.type : type}
            </Typography>
          </Grid>
        </Grid>
      </Grid>
    );
  });

export default Main;

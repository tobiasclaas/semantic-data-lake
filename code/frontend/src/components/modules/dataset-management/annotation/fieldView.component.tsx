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
import DeleteIcon from "@material-ui/icons/Delete";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction";
import IconButton from "@material-ui/core/IconButton";

const Main: React.FC<{ field: Field; path: string; viewModel: ViewModel }> =
  observer(({ field, path, viewModel }) => {
    const { t } = useTranslation();
    let type = field.type;
    while (isArray(type)) {
      type = type.elementType;
    }

    const annotations =
      viewModel.annotations.find((i) => i.data_attribute == path)
        ?.ontology_attribute ?? [];
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

        <Grid item container xs spacing={1} alignItems="center">
          <Grid item>
            <Typography variant="overline">{`${t(
              "generic.annotations"
            )}:`}</Typography>
          </Grid>
          {annotations.length == 0 && (
            <Grid item>
              <Typography variant="overline" style={{ textTransform: "none" }}>
                {t("generic.none")}
              </Typography>
            </Grid>
          )}
        </Grid>

        {annotations.length > 0 && (
          <Grid item xs>
            <List style={{ padding: 0 }}>
              {viewModel.annotations
                .find((i) => i.data_attribute == path)
                ?.ontology_attribute?.map((item, index) => (
                  <ListItem key={index} style={{ padding: 0 }}>
                    <ListItemText primary={item[0]} secondary={item[1]} />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        aria-label="delete"
                        onClick={() =>
                          viewModel.deleteAnnotation(path, item[1])
                        }
                      >
                        <DeleteIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
            </List>
          </Grid>
        )}
      </Grid>
    );
  });

export default Main;

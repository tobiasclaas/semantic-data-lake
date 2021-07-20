import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import { TreeItem, TreeView } from "@material-ui/lab";
import { Field, isArray, isStruct } from "../../../../models/datamarts";
import { Grid } from "@material-ui/core";

const Item: React.FC<{ field: Field; path?: string; viewModel: ViewModel }> = ({
  field,
  path,
  viewModel,
}) => {
  const { t } = useTranslation();

  let name = field.name;
  let type = field.type;
  while (isArray(type)) {
    name += "[]";
    type = type.elementType;
  }

  if (!path) path = name;
  else path = path + "." + name;

  return (
    <TreeItem
      style={{
        paddingTop: "0.25rem",
        paddingBottom: "0.25rem",
      }}
      nodeId={path}
      label={name}
      onClick={() => viewModel.display(field, path)}
    >
      {isStruct(type) &&
        type.fields.map((item, index) => (
          <Item field={item} path={path} key={index} viewModel={viewModel} />
        ))}
    </TreeItem>
  );
};

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <Grid style={{ marginTop: "1rem", width: "100%" }} container spacing={3}>
      <Grid item xs>
        <TreeView
          defaultCollapseIcon={<ExpandMoreIcon />}
          defaultExpandIcon={<ChevronRightIcon />}
        >
          {viewModel.datamart?.metadata.schema.fields.map((item, index) => (
            <Item field={item} key={index} viewModel={viewModel} />
          ))}
        </TreeView>
      </Grid>
      <Grid item xs>
        {viewModel.getFieldView}
      </Grid>
    </Grid>
  );
});

export default Main;

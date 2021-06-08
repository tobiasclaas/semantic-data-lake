import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "..//viewModel";
import IViewProps from "../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import { useLocalObservable } from "mobx-react";
import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import Divider from "@material-ui/core/Divider";
import ListItemText from "@material-ui/core/ListItemText";
import { makeStyles } from "@material-ui/core/styles";
import { Theme } from "@material-ui/core/styles";
import { createStyles } from "@material-ui/core/styles";
import { Container } from "./styles";

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  const onDragStart = (
    event: React.DragEvent<HTMLDivElement>,
    nodeType: string
  ) => {
    event.dataTransfer.setData("application/reactflow", nodeType);
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <Container>
      <List>
        <ListItem
          button
          onDragStart={(event) => onDragStart(event, "data_source")}
          draggable
        >
          <ListItemText primary={t("workflow.items.data_source")} />
        </ListItem>
        <ListItem
          button
          onDragStart={(event) => onDragStart(event, "join")}
          draggable
        >
          <ListItemText primary={t("workflow.items.join")} />
        </ListItem>
      </List>
    </Container>
  );
});

export default Main;

import { withStyles, makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import green from "@material-ui/core/colors/green";
import red from "@material-ui/core/colors/red";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Chip from "@material-ui/core/Chip";
import { Theme, styled } from "@material-ui/core/styles";
import { GridProps } from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import React from "react";

export const ItemContainer = withStyles(() => ({
  root: {
    display: "flex",
    margin: "0px 8px 16px 8px",
    flex: 1,
    flexDirection: "column",
  },
}))(Paper);

export const ItemGrid = withStyles(() => ({
  root: {
    padding: "1rem",
    flex: 1,
  },
}))(Grid);

export const BodyGridItem = withStyles(() => ({
  root: {
    maxWidth: "100%",
    flex: 1,
    display: "flex",
    flexDirection: "column",
    marginBottom: 2,
  },
}))(Grid);

export const FooterGridItem = withStyles(() => ({
  root: {
    display: "flex",
  },
}))(Grid);

export const FooterButton = withStyles(() => ({
  root: {
    flex: 1,
    color: "red",
  },
}))(Button);

export const BodyTypography = withStyles(() => ({
  root: {
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
    textAlign: "center",
  },
}))(Typography);

export const ItemGridItem = withStyles(() => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
}))(Grid);

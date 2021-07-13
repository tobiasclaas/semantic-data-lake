import React, { useState } from "react";
import Paper from "@material-ui/core/Paper";
import {
  BodyGridItem,
  BodyTypography,
  FooterGridItem,
  ItemContainer,
  ItemGrid,
  ItemGridItem,
} from "./styles";
import Tooltip from "@material-ui/core/Tooltip";
import Fade from "@material-ui/core/Fade";
import EditIcon from "@material-ui/icons/Edit";
import DeleteIcon from "@material-ui/icons/Delete";
import Grid from "@material-ui/core/Grid";
import ItemButton from "./button";
import { red } from "@material-ui/core/colors";

export interface ItemProps {
  title: string;
  onDelete?: () => void;
}

const Item: React.FC<ItemProps & React.ComponentProps<typeof Paper>> = ({
  title,
  onDelete,
  children,
  ...rest
}) => {
  const [elevation, setElevation] = useState<number>(2);

  return (
    <ItemGridItem item xs={6} sm={4} md={3} lg={2}>
      <ItemContainer
        {...rest}
        elevation={elevation}
        onMouseOver={() => setElevation(9)}
        onMouseOut={() => setElevation(2)}
      >
        <ItemGrid spacing={1} container direction="column" alignItems="stretch">
          <BodyGridItem item>
            <Tooltip
              TransitionComponent={Fade}
              TransitionProps={{ timeout: 600 }}
              placement="top"
              arrow
              title={title}
            >
              <BodyTypography variant="subtitle1">{title}</BodyTypography>
            </Tooltip>
          </BodyGridItem>
          <FooterGridItem item container spacing={1}>
            {onDelete && (
              <ItemButton htmlColor={red[500]} onClick={onDelete}>
                <DeleteIcon fontSize="small" />
              </ItemButton>
            )}
            {children}
          </FooterGridItem>
        </ItemGrid>
      </ItemContainer>
    </ItemGridItem>
  );
};

export default Item;

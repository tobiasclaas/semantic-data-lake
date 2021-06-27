import React from "react";

import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";

export interface ButtonProps {
  htmlColor?: string;
}

const ItemButton: React.FC<ButtonProps & React.ComponentProps<typeof Button>> =
  ({ htmlColor, ...rest }) => {
    return (
      <Grid item xs>
        <Button
          fullWidth
          style={{ color: htmlColor }}
          {...rest}
          variant="outlined"
        />
      </Grid>
    );
  };

export default ItemButton;

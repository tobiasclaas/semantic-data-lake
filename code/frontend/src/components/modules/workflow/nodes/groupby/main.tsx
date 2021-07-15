import React, { memo } from "react";

import { Handle, Position } from "react-flow-renderer";
import { useTranslation } from "react-i18next";
import ViewColumnIcon from "@material-ui/icons/ViewColumn";
import { Typography } from "@material-ui/core";
import { IData } from "./data";

export default memo(({ data }: { data: IData }) => {
  const { t } = useTranslation();
  return (
    <>
      <div
        style={{
          display: "flex",
          border: "1px solid #777",
          borderRadius: "0.4rem",
          backgroundColor: "#fff",
          padding: 10,
        }}
      >
        <ViewColumnIcon />
        <Typography style={{ margin: "0 0.5rem" }}>
          {t("workflow.items.groupby")}
        </Typography>
      </div>
      <Handle
        type="target"
        position={Position.Left}
        id="input"
        style={{ background: "#555" }}
      />
      <Handle
        type="source"
        position={Position.Right}
        id="output"
        style={{ background: "#555" }}
      />
    </>
  );
});
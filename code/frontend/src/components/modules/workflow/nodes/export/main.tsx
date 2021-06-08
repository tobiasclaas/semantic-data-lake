import Typography from "@material-ui/core/Typography";
import React, { memo } from "react";

import { Handle, Position } from "react-flow-renderer";
import { useTranslation } from "react-i18next";
import StorageIcon from "@material-ui/icons/Storage";
import SaveIcon from "@material-ui/icons/Save";

export default memo(({ data }: { data: any }) => {
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
        <SaveIcon />
        <Typography style={{ margin: "0 0.5rem" }}>
          {t("workflow.items.export")}
        </Typography>
      </div>
      <Handle
        type="target"
        position={Position.Right}
        id="input"
        style={{ background: "#555" }}
      />
    </>
  );
});

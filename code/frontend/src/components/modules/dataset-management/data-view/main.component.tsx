import React from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import TableContainer from "@material-ui/core/TableContainer";
import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import { withStyles } from "@material-ui/core/styles";

const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const StyledTableRow = withStyles((theme) => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const { t } = useTranslation();

  return (
    <React.Fragment>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              {viewModel.headers.map((item, index) => (
                <StyledTableCell key={index}>{item}</StyledTableCell>
              ))}
              {/*<TableCell align="right">Uri</TableCell>*/}
            </TableRow>
          </TableHead>
          <TableBody>
            {viewModel.data.map((row, index) => (
              <StyledTableRow key={index}>
                {row.map((data, index) => (
                  <TableCell key={index} component="th" scope="row">
                    {data}
                  </TableCell>
                ))}
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </React.Fragment>
  );
});

export default Main;

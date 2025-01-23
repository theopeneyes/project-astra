import React, { useState } from "react";
import { Grid, GridColumn as Column } from "@progress/kendo-react-grid";
import editIcon from "../assets/images/edit-icon.svg";
import viewIcon from "../assets/images/view-icon.svg";
import deleteIcon from "../assets/images/delete-icon.svg";

const Users = [
    { UserName: 'Thomas Anree', LastLogin: '22 Dec, 2024 10:15 AM', Email: 'thomas.anree@astra.com', Role: 'Admin User', Status: 'Active' },
    { UserName: 'Julia Fisher', LastLogin: '21 Dec, 2024 02:45 PM', Email: 'julia.fisher@astra.com', Role: 'Tech User', Status: 'Inactive' },
    { UserName: 'Ethan Williams', LastLogin: '20 Dec, 2024 09:30 AM', Email: 'ethan.williams@astra.com', Role: 'Main User', Status: 'Active' },
    { UserName: 'Ava Johnson', LastLogin: '19 Dec, 2024 08:00 PM', Email: 'ava.johnson@astra.com', Role: 'Tech User', Status: 'Active' },
    { UserName: 'Mason Brown', LastLogin: '18 Dec, 2024 07:15 AM', Email: 'mason.brown@astra.com', Role: 'Main User', Status: 'Inactive' },
    { UserName: 'Liam Martinez', LastLogin: '17 Dec, 2024 06:45 PM', Email: 'liam.martinez@astra.com', Role: 'Admin User', Status: 'Active' },
    { UserName: 'Emma Garcia', LastLogin: '16 Dec, 2024 04:30 PM', Email: 'emma.garcia@astra.com', Role: 'Tech User', Status: 'Inactive' },
    { UserName: 'James Anderson', LastLogin: '15 Dec, 2024 11:15 AM', Email: 'james.anderson@astra.com', Role: 'Main User', Status: 'Active' },
    { UserName: 'Isabella Thomas', LastLogin: '14 Dec, 2024 05:00 PM', Email: 'isabella.thomas@astra.com', Role: 'Admin User', Status: 'Inactive' },
    { UserName: 'Logan Moore', LastLogin: '13 Dec, 2024 09:00 AM', Email: 'logan.moore@astra.com', Role: 'Tech User', Status: 'Active' },
    { UserName: 'Charlotte Clark', LastLogin: '12 Dec, 2024 12:15 PM', Email: 'charlotte.clark@astra.com', Role: 'Main User', Status: 'Inactive' },
    { UserName: 'Lucas Lewis', LastLogin: '11 Dec, 2024 07:00 AM', Email: 'lucas.lewis@astra.com', Role: 'Admin User', Status: 'Active' },
    { UserName: 'Harper Scott', LastLogin: '10 Dec, 2024 08:45 PM', Email: 'harper.scott@astra.com', Role: 'Tech User', Status: 'Inactive' },
    { UserName: 'Benjamin Hall', LastLogin: '09 Dec, 2024 06:30 PM', Email: 'benjamin.hall@astra.com', Role: 'Main User', Status: 'Active' },
    { UserName: 'Mia Allen', LastLogin: '08 Dec, 2024 10:15 AM', Email: 'mia.allen@astra.com', Role: 'Admin User', Status: 'Inactive' },
    { UserName: 'Oliver Young', LastLogin: '07 Dec, 2024 03:45 PM', Email: 'oliver.young@astra.com', Role: 'Tech User', Status: 'Active' },
    { UserName: 'Sophia King', LastLogin: '06 Dec, 2024 02:00 PM', Email: 'sophia.king@astra.com', Role: 'Main User', Status: 'Inactive' },
    { UserName: 'Daniel Lee', LastLogin: '05 Dec, 2024 01:30 PM', Email: 'daniel.lee@astra.com', Role: 'Admin User', Status: 'Active' },
    { UserName: 'Chloe Harris', LastLogin: '04 Dec, 2024 04:00 PM', Email: 'chloe.harris@astra.com', Role: 'Tech User', Status: 'Inactive' },
    { UserName: 'Jackson Nelson', LastLogin: '03 Dec, 2024 08:15 AM', Email: 'jackson.nelson@astra.com', Role: 'Main User', Status: 'Active' },
    { UserName: 'Amelia Carter', LastLogin: '02 Dec, 2024 09:30 PM', Email: 'amelia.carter@astra.com', Role: 'Tech User', Status: 'Inactive' },
    { UserName: 'Henry Mitchell', LastLogin: '01 Dec, 2024 07:45 AM', Email: 'henry.mitchell@astra.com', Role: 'Admin User', Status: 'Active' },
    { UserName: 'Sebastian Perez', LastLogin: '30 Nov, 2024 06:00 PM', Email: 'sebastian.perez@astra.com', Role: 'Main User', Status: 'Inactive' },
    { UserName: 'Aria Roberts', LastLogin: '29 Nov, 2024 05:30 PM', Email: 'aria.roberts@astra.com', Role: 'Tech User', Status: 'Active' },
    { UserName: 'Samuel Evans', LastLogin: '28 Nov, 2024 03:15 PM', Email: 'samuel.evans@astra.com', Role: 'Admin User', Status: 'Inactive' },
    { UserName: 'Eleanor Collins', LastLogin: '27 Nov, 2024 02:45 PM', Email: 'eleanor.collins@astra.com', Role: 'Main User', Status: 'Active' },
    { UserName: 'William Stewart', LastLogin: '26 Nov, 2024 12:30 PM', Email: 'william.stewart@astra.com', Role: 'Tech User', Status: 'Inactive' },
    { UserName: 'Grace Morris', LastLogin: '25 Nov, 2024 10:00 AM', Email: 'grace.morris@astra.com', Role: 'Admin User', Status: 'Active' },
    { UserName: 'Jack Reed', LastLogin: '24 Nov, 2024 09:15 AM', Email: 'jack.reed@astra.com', Role: 'Main User', Status: 'Inactive' },
    { UserName: 'Zoe Wood', LastLogin: '23 Nov, 2024 08:30 PM', Email: 'zoe.wood@astra.com', Role: 'Tech User', Status: 'Active' },
];

const initialDataState = {
  skip: 0,
  take: 10,
};

const UserManage = () => {
  const [page, setPage] = useState(initialDataState);
  const [pageSizeValue, setPageSizeValue] = useState();
  // const { setComponentName } = useComponentName(pageName.dashboard);

    const pageChange = (event) => {
        const targetEvent = event.targetEvent;
        const take = targetEvent.value === 'All' ? Users.length : event.page.take;

    if (targetEvent.value) {
      setPageSizeValue(targetEvent.value);
    }

    setPage({
      ...event.page,
      take,
    });
  };

    const userNameCell = (props) => {
        const { dataItem } = props;
        return (
            <td><strong>{dataItem.UserName}</strong></td>
        );
    };

    const statusCell = (props) => {
        const { dataItem } = props;
        const statusClass = dataItem.Status === "Active" ? "green-status" : "red-status";
        return (
            <td className="text-center"><span className={`grid-status ${statusClass}`}>{dataItem.Status}</span></td>
        );
    };

    const actionsCell = (props) => {
        const { dataItem } = props;
        return (
            <td className="text-center">
                <button className="action-btn" onClick={() => handleEdit(dataItem)}><img src={editIcon}/></button>
                <button className="action-btn" onClick={() => handleView(dataItem)}><img src={viewIcon}/></button>
                <button className="action-btn" onClick={() => handleDelete(dataItem)}><img src={deleteIcon}/></button>
            </td>
        );
    };

    const handleEdit = (user) => {
        alert(`Editing user: ${user.UserName}`);
    };

    const handleView = (user) => {
        alert(`Viewing user: ${user.UserName}`);
    };

    const handleDelete = (user) => {
        alert(`Deleting user: ${user.UserName}`);
    };

    return (
        <div className="default-box">
            <Grid
                data={Users.slice(page.skip, page.take + page.skip)}
                skip={page.skip}
                take={page.take}
                total={Users.length}
                pageable={{
                    buttonCount: 3,
                    pageSizes: [5, 10, 15, 'All'],
                    pageSizeValue: pageSizeValue,
                }}
                onPageChange={pageChange}
                scrollable="none"
            >
                <Column field="UserName" title="User Name" cell={userNameCell} />
                <Column field="Email" title="Email Address" />
                <Column field="Role" title="Role" />
                <Column field="LastLogin" title="Last Login" />
                <Column field="Status" headerClassName="justify-content-center"  title="Status" cell={statusCell} />
                <Column headerClassName="justify-content-center" title="Actions" cell={actionsCell} />
            </Grid>
        </div>
    );
};

export default UserManage;

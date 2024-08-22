const TableBody = ({ tableData, columns }) => {
    return (
        <tbody>
            {tableData.map((data) => {
                return (
                    <tr key={data.id}>
                        {columns.map(({ accessor }) => {
                            let tData = data[accessor];
                            if (tData === null || tData === undefined) {
                                tData = "_";
                            } else if (tData === 0) {
                                tData = "0";
                            } else if (tData === false) {
                                tData = "no";
                            } else if (tData === true) {
                                tData = "yes";
                            }
                            return <td key={accessor}>{tData}</td>;
                        })}
                    </tr>
                );
            })}
        </tbody>
    );
};

export default TableBody;

import React from 'react';

interface ColumnDefinition<T> {
  key: string;
  header: string;
  accessor: (row: T) => any;
}

export interface TableProps<T> {
  data: T[];
  columns: ColumnDefinition<T>[];
}

export function Table<T>({ data, columns }: TableProps<T>) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col.key} style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #333' }}>
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            {columns.map(col => (
              <td key={col.key} style={{ padding: '8px', borderBottom: '1px solid #222' }}>
                {col.accessor(row)}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

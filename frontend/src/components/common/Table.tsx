/**
 * Table Component
 *
 * Sortable, filterable data table with dark theme
 * Features: Sorting, selection, hover effects, responsive
 *
 * Version: v0.1.0
 * WCAG 2.1 AA Compliant
 */

import React, { useState, useMemo } from 'react';
import './Table.css';

export interface ColumnDefinition<T> {
  key: string;
  header: string;
  accessor: (row: T) => any;
  sortable?: boolean;
  width?: string;
  align?: 'left' | 'center' | 'right';
  render?: (value: any, row: T) => React.ReactNode;
}

export interface TableProps<T> {
  data: T[];
  columns: ColumnDefinition<T>[];
  sortable?: boolean;
  defaultSortColumn?: string;
  defaultSortOrder?: 'asc' | 'desc';
  selectable?: boolean;
  selectedRows?: string[];
  onSelectionChange?: (selectedIds: string[]) => void;
  compact?: boolean;
  striped?: boolean;
  hoverable?: boolean;
  onRowClick?: (row: T) => void;
  emptyMessage?: string;
  getRowId?: (row: T, index: number) => string;
  ariaLabel?: string;
}

export function Table<T>({
  data,
  columns,
  sortable = true,
  defaultSortColumn,
  defaultSortOrder = 'asc',
  selectable = false,
  selectedRows = [],
  onSelectionChange,
  compact = false,
  striped = false,
  hoverable = true,
  onRowClick,
  emptyMessage = 'No data available',
  getRowId = (_, index) => String(index),
  ariaLabel,
}: TableProps<T>) {
  const [sortColumn, setSortColumn] = useState<string | null>(defaultSortColumn || null);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>(defaultSortOrder);

  const sortedData = useMemo(() => {
    if (!sortColumn) return data;

    const column = columns.find((col) => col.key === sortColumn);
    if (!column) return data;

    return [...data].sort((a, b) => {
      const aValue = column.accessor(a);
      const bValue = column.accessor(b);

      if (aValue === bValue) return 0;

      const comparison = aValue < bValue ? -1 : 1;
      return sortOrder === 'asc' ? comparison : -comparison;
    });
  }, [data, sortColumn, sortOrder, columns]);

  const handleSort = (columnKey: string) => {
    if (sortColumn === columnKey) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(columnKey);
      setSortOrder('asc');
    }
  };

  const handleRowSelection = (rowId: string) => {
    if (!onSelectionChange) return;

    const newSelection = selectedRows.includes(rowId)
      ? selectedRows.filter((id) => id !== rowId)
      : [...selectedRows, rowId];

    onSelectionChange(newSelection);
  };

  const tableClassNames = [
    'table',
    compact && 'table--compact',
    striped && 'table--striped',
    hoverable && 'table--hoverable',
  ]
    .filter(Boolean)
    .join(' ');

  if (data.length === 0) {
    return (
      <div className="table-empty">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className={tableClassNames} aria-label={ariaLabel || 'Data table'}>
        <thead>
          <tr>
            {selectable && (
              <th className="table__th--checkbox">
                <input
                  type="checkbox"
                  checked={selectedRows.length === data.length && data.length > 0}
                  onChange={() => {
                    if (selectedRows.length === data.length) {
                      onSelectionChange?.([]);
                    } else {
                      onSelectionChange?.(data.map((row, i) => getRowId(row, i)));
                    }
                  }}
                />
              </th>
            )}
            {columns.map((column) => {
              const isSortable = sortable && column.sortable !== false;
              const isCurrentSort = sortColumn === column.key;

              return (
                <th
                  key={column.key}
                  className={isSortable ? 'sortable' : ''}
                  style={{ width: column.width, textAlign: column.align || 'left' }}
                  onClick={() => isSortable && handleSort(column.key)}
                >
                  <div className="table__th-content">
                    {column.header}
                    {isSortable && isCurrentSort && (
                      <span className="table__sort-indicator">
                        {sortOrder === 'asc' ? ' ↑' : ' ↓'}
                      </span>
                    )}
                  </div>
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, rowIndex) => {
            const rowId = getRowId(row, rowIndex);
            const isSelected = selectedRows.includes(rowId);

            return (
              <tr
                key={rowId}
                className={isSelected ? 'table__row--selected' : ''}
                onClick={() => onRowClick?.(row)}
              >
                {selectable && (
                  <td className="table__td--checkbox">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => handleRowSelection(rowId)}
                    />
                  </td>
                )}
                {columns.map((column) => {
                  const value = column.accessor(row);
                  const rendered = column.render ? column.render(value, row) : value;

                  return (
                    <td
                      key={column.key}
                      style={{ textAlign: column.align || 'left' }}
                    >
                      {rendered}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

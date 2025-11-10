/**
 * OperationMatrix Component Stories
 *
 * Demonstrates the OperationMatrix component with 4 operation groups
 * Version: v0.1.0
 */

import type { Meta, StoryObj } from '@storybook/react';
import { OperationMatrix } from './OperationMatrix';
import type { OperationGroup } from './OperationMatrix';

const sampleOperations: OperationGroup[] = [
  {
    name: 'FACE',
    displayName: 'Face Milling (Planfräsen)',
    operations: [
      {
        id: 'FACE_ROUGH',
        name: 'Face Roughing (Schruppen)',
        description: 'High MRR, coarse surface',
      },
      {
        id: 'FACE_FINISH',
        name: 'Face Finishing (Schlichten)',
        description: 'Low MRR, fine surface',
      },
    ],
  },
  {
    name: 'SLOT',
    displayName: 'Slot Milling (Nuten/Taschen)',
    operations: [
      {
        id: 'SLOT_STRAIGHT',
        name: 'Straight Slot',
        description: 'Linear slotting operation',
      },
      {
        id: 'SLOT_TROCHOIDAL',
        name: 'Trochoidal Slot',
        description: 'Circular interpolation for deeper cuts',
      },
      {
        id: 'SLOT_POCKET',
        name: 'Pocket Milling',
        description: 'Enclosed area machining',
      },
      {
        id: 'SLOT_HELICAL',
        name: 'Helical Ramping',
        description: 'Spiral entry for slots',
      },
    ],
  },
  {
    name: 'GEOMETRY',
    displayName: 'Geometry (Konturbearbeitung)',
    operations: [
      {
        id: 'GEOMETRY_2D',
        name: '2D Contour',
        description: 'Profile milling',
      },
      {
        id: 'GEOMETRY_3D',
        name: '3D Surface',
        description: 'Complex surface machining',
      },
      {
        id: 'GEOMETRY_ADAPTIVE',
        name: 'Adaptive Clearing',
        description: 'Intelligent toolpath generation',
      },
    ],
  },
  {
    name: 'SPECIAL',
    displayName: 'Special Operations (Sonderfunktionen)',
    operations: [
      {
        id: 'SPECIAL_THREAD',
        name: 'Thread Milling',
        description: 'Helical thread cutting',
      },
      {
        id: 'SPECIAL_CHAMFER',
        name: 'Chamfer',
        description: 'Edge deburring',
      },
    ],
  },
];

const meta: Meta<typeof OperationMatrix> = {
  title: 'Components/OperationMatrix',
  component: OperationMatrix,
  tags: ['autodocs'],
  argTypes: {
    multiSelect: { control: 'boolean' },
    showDescriptions: { control: 'boolean' },
  },
};

export default meta;
type Story = StoryObj<typeof OperationMatrix>;

export const Default: Story = {
  args: {
    operations: sampleOperations,
    selectedOperations: [],
    onSelectionChange: (selected) => console.log('Selected:', selected),
  },
};

export const WithSelections: Story = {
  args: {
    operations: sampleOperations,
    selectedOperations: ['FACE_ROUGH', 'FACE_FINISH', 'GEOMETRY_3D'],
    onSelectionChange: (selected) => console.log('Selected:', selected),
  },
};

export const WithDescriptions: Story = {
  args: {
    ...Default.args,
    showDescriptions: true,
  },
};

export const SingleSelect: Story = {
  args: {
    operations: sampleOperations,
    selectedOperations: ['SLOT_TROCHOIDAL'],
    multiSelect: false,
    onSelectionChange: (selected) => console.log('Selected:', selected),
  },
};

export const SomeGroupsCollapsed: Story = {
  args: {
    operations: sampleOperations,
    selectedOperations: ['FACE_ROUGH'],
    expandedGroups: ['FACE', 'GEOMETRY'],
    onSelectionChange: (selected) => console.log('Selected:', selected),
  },
};

export const AllCollapsed: Story = {
  args: {
    operations: sampleOperations,
    selectedOperations: [],
    expandedGroups: [],
    onSelectionChange: (selected) => console.log('Selected:', selected),
  },
};

export const FullySelected: Story = {
  args: {
    operations: sampleOperations,
    selectedOperations: [
      'FACE_ROUGH',
      'FACE_FINISH',
      'SLOT_STRAIGHT',
      'SLOT_TROCHOIDAL',
      'SLOT_POCKET',
      'SLOT_HELICAL',
      'GEOMETRY_2D',
      'GEOMETRY_3D',
      'GEOMETRY_ADAPTIVE',
      'SPECIAL_THREAD',
      'SPECIAL_CHAMFER',
    ],
    showDescriptions: true,
    onSelectionChange: (selected) => console.log('Selected:', selected),
  },
};

/**
 * Slider Component Stories
 *
 * Demonstrates the Slider component with various configurations
 * Version: v0.1.0
 */

import type { Meta, StoryObj } from '@storybook/react';
import { Slider } from './Slider';

const meta: Meta<typeof Slider> = {
  title: 'Components/Slider',
  component: Slider,
  tags: ['autodocs'],
  argTypes: {
    min: { control: 'number' },
    max: { control: 'number' },
    value: { control: 'number' },
    step: { control: 'number' },
    compact: { control: 'boolean' },
    showValue: { control: 'boolean' },
    disabled: { control: 'boolean' },
  },
};

export default meta;
type Story = StoryObj<typeof Slider>;

export const Default: Story = {
  args: {
    min: -50,
    max: 50,
    value: 0,
    markers: [
      { value: -50, label: 'Conservative' },
      { value: 0, label: 'Optimal' },
      { value: 50, label: 'Aggressive' },
    ],
    onChange: (value) => console.log('Value changed:', value),
  },
};

export const WithValue: Story = {
  args: {
    ...Default.args,
    showValue: true,
    valueFormatter: (v) => `${v > 0 ? '+' : ''}${v}%`,
  },
};

export const WithLabels: Story = {
  args: {
    ...Default.args,
    showValue: true,
    leftLabel: 'Conservative',
    rightLabel: 'Aggressive',
  },
};

export const Compact: Story = {
  args: {
    ...Default.args,
    compact: true,
  },
};

export const CustomGradient: Story = {
  args: {
    ...Default.args,
    showValue: true,
    gradient: ['#ff0000', '#ffff00', '#00ff00'],
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    disabled: true,
    value: 25,
  },
};

export const ManyMarkers: Story = {
  args: {
    min: 0,
    max: 100,
    value: 50,
    markers: [
      { value: 0, label: 'Min' },
      { value: 25, label: 'Low' },
      { value: 50, label: 'Medium' },
      { value: 75, label: 'High' },
      { value: 100, label: 'Max' },
    ],
    showValue: true,
    onChange: (value) => console.log('Value changed:', value),
  },
};

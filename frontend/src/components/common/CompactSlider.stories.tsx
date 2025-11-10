/**
 * CompactSlider Component Stories
 *
 * Demonstrates the CompactSlider component for Expert Mode
 * Version: v0.1.0
 */

import type { Meta, StoryObj } from '@storybook/react';
import { CompactSlider } from './CompactSlider';

const meta: Meta<typeof CompactSlider> = {
  title: 'Components/CompactSlider',
  component: CompactSlider,
  tags: ['autodocs'],
  argTypes: {
    min: { control: 'number' },
    max: { control: 'number' },
    value: { control: 'number' },
    centerValue: { control: 'number' },
    showValue: { control: 'boolean' },
    disabled: { control: 'boolean' },
  },
};

export default meta;
type Story = StoryObj<typeof CompactSlider>;

export const Default: Story = {
  args: {
    min: -100,
    max: 100,
    value: 0,
    label: 'ae',
    unit: '%',
    showValue: true,
    onChange: (value) => console.log('Value changed:', value),
  },
};

export const PositiveValue: Story = {
  args: {
    ...Default.args,
    value: 50,
  },
};

export const NegativeValue: Story = {
  args: {
    ...Default.args,
    value: -50,
  },
};

export const CustomColors: Story = {
  args: {
    ...Default.args,
    negativeColor: '#ff0000',
    positiveColor: '#00ff00',
    centerColor: '#ffffff',
  },
};

export const DifferentRange: Story = {
  args: {
    min: -50,
    max: 150,
    value: 0,
    centerValue: 50,
    label: 'Custom',
    unit: 'mm',
    showValue: true,
    onChange: (value) => console.log('Value changed:', value),
  },
};

export const NoLabel: Story = {
  args: {
    min: -100,
    max: 100,
    value: 25,
    showValue: false,
    onChange: (value) => console.log('Value changed:', value),
  },
};

export const Disabled: Story = {
  args: {
    ...Default.args,
    value: 75,
    disabled: true,
  },
};

export const SmallHeight: Story = {
  args: {
    ...Default.args,
    height: 4,
  },
};

export const LargeHeight: Story = {
  args: {
    ...Default.args,
    height: 12,
  },
};

import { Node } from '@xyflow/react';

export type ExpandCollapseNode = Node<{
  expanded: boolean;
  expandable?: boolean;
}>;
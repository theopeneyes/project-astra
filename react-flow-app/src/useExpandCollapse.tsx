import { useMemo } from 'react';
import { Edge } from 'reactflow';
import Dagre from '@dagrejs/dagre';

import { ExpandCollapseNode } from './types';

export type UseExpandCollapseOptions = {
  layoutNodes?: boolean;
  treeWidth?: number;
  treeHeight?: number;
};

function filterCollapsedChildren(
  dagre: Dagre.graphlib.Graph,
  node: ExpandCollapseNode
) {
  // 🚨 The current types for some of dagre's methods are incorrect. In future
  // versions of dagre this should be fixed, but for now we need to cast the return
  // value to keep TypeScript happy.
  const children = dagre.successors(node.id) as unknown as string[] | undefined;

  // Update this node's props so it knows if it has children and can be expanded
  // or not.
  node.data.expandable = !!children?.length;

  // If the node is collpased (ie it is not expanded) then we want to remove all
  // of its children from the graph *and* any of their children.
  if (!node.data.expanded) {
    while (children?.length) {
      const child = children.pop()!;

      children.push(...(dagre.successors(child) as unknown as string[]));
      dagre.removeNode(child);
    }
  }
}

function useExpandCollapse(
  nodes: ExpandCollapseNode[],
  edges: Edge[],
  {
    layoutNodes = true,
    treeWidth = 300,
    treeHeight = 300,
  }: UseExpandCollapseOptions = {}
): { nodes: ExpandCollapseNode[]; edges: Edge[] } {
  return useMemo(() => {
    if (!layoutNodes) return { nodes, edges };

    const dagre = new Dagre.graphlib.Graph()
      .setDefaultEdgeLabel(() => ({}))
      .setGraph({ 
        rankdir: 'LR', 
        nodesep: 50, 
        edgesep: 50, 
        ranksep: 100,
      });

    for (const node of nodes) {
      dagre.setNode(node.id, {
        width: treeWidth,
        height: treeHeight,
        data: node.data,
      });
    }

    for (const edge of edges) {
      dagre.setEdge(edge.source, edge.target);
    }

    // 3. Iterate over the nodes *again* to determine which ones should be hidden
    // based on expand/collapse state. Hidden nodes are removed from the dagre
    // graph entirely.
    for (const node of nodes) {
      filterCollapsedChildren(dagre, node);
    }

    // 4. Run the dagre layouting algorithm.
    Dagre.layout(dagre);

    return {
      // 5. Return a new array of layouted nodes. This will not include any nodes
      // that were removed from the dagre graph in step 3.
      //
      // 💡 `Array.flatMap` can act as a *filter map*. If we want to remove an
      // element from the array, we can return an empty array in this iteration.
      // Otherwise, we can map the element like normal and wrap it in a singleton
      // array.
      nodes: nodes.flatMap((node) => {
        // This node might have been filtered out by `filterCollapsedChildren` if
        // any of its ancestors were collpased.
        if (!dagre.hasNode(node.id)) return [];

        const { x, y } = dagre.node(node.id);

        const type = 'custom';
        const position = { x, y };
        // 🚨 `filterCollapsedChildren` *mutates* the data object of a node. React
        // will not know the data has changed unless we create a new object here.
        const data = { ...node.data };

        return [{ ...node, position, type, data }];
      }),
      edges,
    };
  }, [nodes, edges, layoutNodes, treeWidth, treeHeight]);
}

export default useExpandCollapse;

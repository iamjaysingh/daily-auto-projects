/**
 * Binary Search Tree
 * A complete BST implementation with traversals and visualization.
 * @author Jay Singh (iamjaysingh)
 */

import java.util.*;

public class Main {
    static int[] values;
    static int size = 0;
    static int capacity = 100;
    static int[] left, right;

    // Node-based BST for clarity
    static class Node {
        int data;
        Node left, right;

        Node(int data) {
            this.data = data;
            this.left = this.right = null;
        }
    }

    static Node root = null;

    static Node insert(Node node, int data) {
        if (node == null) return new Node(data);
        if (data < node.data) node.left = insert(node.left, data);
        else if (data > node.data) node.right = insert(node.right, data);
        return node;
    }

    static Node search(Node node, int data) {
        if (node == null || node.data == data) return node;
        if (data < node.data) return search(node.left, data);
        return search(node.right, data);
    }

    static Node findMin(Node node) {
        while (node.left != null) node = node.left;
        return node;
    }

    static Node delete(Node node, int data) {
        if (node == null) return null;
        if (data < node.data) node.left = delete(node.left, data);
        else if (data > node.data) node.right = delete(node.right, data);
        else {
            if (node.left == null) return node.right;
            if (node.right == null) return node.left;
            Node minNode = findMin(node.right);
            node.data = minNode.data;
            node.right = delete(node.right, minNode.data);
        }
        return node;
    }

    static int height(Node node) {
        if (node == null) return 0;
        return 1 + Math.max(height(node.left), height(node.right));
    }

    static int countNodes(Node node) {
        if (node == null) return 0;
        return 1 + countNodes(node.left) + countNodes(node.right);
    }

    // Traversals
    static List<Integer> inorder(Node node) {
        List<Integer> result = new ArrayList<>();
        if (node != null) {
            result.addAll(inorder(node.left));
            result.add(node.data);
            result.addAll(inorder(node.right));
        }
        return result;
    }

    static List<Integer> preorder(Node node) {
        List<Integer> result = new ArrayList<>();
        if (node != null) {
            result.add(node.data);
            result.addAll(preorder(node.left));
            result.addAll(preorder(node.right));
        }
        return result;
    }

    static List<Integer> postorder(Node node) {
        List<Integer> result = new ArrayList<>();
        if (node != null) {
            result.addAll(postorder(node.left));
            result.addAll(postorder(node.right));
            result.add(node.data);
        }
        return result;
    }

    static List<Integer> levelOrder(Node node) {
        List<Integer> result = new ArrayList<>();
        if (node == null) return result;
        Queue<Node> queue = new LinkedList<>();
        queue.add(node);
        while (!queue.isEmpty()) {
            Node curr = queue.poll();
            result.add(curr.data);
            if (curr.left != null) queue.add(curr.left);
            if (curr.right != null) queue.add(curr.right);
        }
        return result;
    }

    // Visual tree printing
    static void printTree(Node node, String prefix, boolean isLeft) {
        if (node == null) return;
        System.out.println(prefix + (isLeft ? "├── " : "└── ") + node.data);
        printTree(node.left, prefix + (isLeft ? "│   " : "    "), true);
        printTree(node.right, prefix + (isLeft ? "│   " : "    "), false);
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(50));
        System.out.println("  🌳 Binary Search Tree");
        System.out.println("=".repeat(50));

        // Insert sample values
        int[] data = {50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45};
        System.out.println("\n  Inserting: " + Arrays.toString(data));

        for (int val : data) {
            root = insert(root, val);
        }

        // Display tree
        System.out.println("\n  🌳 Tree Structure:");
        printTree(root, "    ", false);

        // Stats
        System.out.println("\n  📊 Stats:");
        System.out.println("    Nodes:  " + countNodes(root));
        System.out.println("    Height: " + height(root));
        System.out.println("    Min:    " + findMin(root).data);

        // Traversals
        System.out.println("\n  🔄 Traversals:");
        System.out.println("    Inorder:    " + inorder(root));
        System.out.println("    Preorder:   " + preorder(root));
        System.out.println("    Postorder:  " + postorder(root));
        System.out.println("    Level Order: " + levelOrder(root));

        // Search
        System.out.println("\n  🔍 Search:");
        System.out.println("    Search 40: " + (search(root, 40) != null ? "Found ✅" : "Not Found ❌"));
        System.out.println("    Search 99: " + (search(root, 99) != null ? "Found ✅" : "Not Found ❌"));

        // Delete
        System.out.println("\n  🗑️  Deleting 30...");
        root = delete(root, 30);
        System.out.println("    Inorder after delete: " + inorder(root));
        printTree(root, "    ", false);

        System.out.println("\n  👋 Done!");
    }
}

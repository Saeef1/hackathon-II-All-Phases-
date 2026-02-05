'use client';

import Link from 'next/link';
import { Todo } from '@/lib/types';
import TaskCompletionToggle from './TaskCompletionToggle';

interface TaskItemProps {
  task: Todo;
  onToggleComplete: (id: string, isCompleted: boolean) => void;
  onDelete: (id: string) => void;
  isUpdating?: boolean;
}

export default function TaskItem({
  task,
  onToggleComplete,
  onDelete,
  isUpdating = false,
}: TaskItemProps) {
  const formattedDate = new Date(task.created_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <div
      className={`group flex items-start gap-4 rounded-lg border bg-white p-4 shadow-sm transition-all hover:shadow-md ${
        task.is_completed ? 'border-green-200 bg-green-50' : 'border-gray-200'
      }`}
    >
      <TaskCompletionToggle
        isCompleted={task.is_completed}
        onToggle={() => onToggleComplete(task.id, !task.is_completed)}
        disabled={isUpdating}
      />

      <div className="min-w-0 flex-1">
        <Link href={`/tasks/${task.id}`} className="block">
          <h3
            className={`text-lg font-medium ${
              task.is_completed ? 'text-gray-500 line-through' : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.is_completed ? 'text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}
        </Link>
        <p className="mt-2 text-xs text-gray-400">Created {formattedDate}</p>
      </div>

      <div className="flex items-center gap-2 opacity-0 transition-opacity group-hover:opacity-100">
        <Link
          href={`/tasks/${task.id}`}
          className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-blue-600"
          aria-label="Edit task"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
            />
          </svg>
        </Link>
        <button
          onClick={() => onDelete(task.id)}
          className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-red-600"
          aria-label="Delete task"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}

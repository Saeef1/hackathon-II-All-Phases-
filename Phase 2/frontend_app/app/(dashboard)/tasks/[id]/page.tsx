'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { todoApi } from '@/lib/api-client';
import { Todo, TodoUpdate } from '@/lib/types';
import TaskForm from '@/components/tasks/TaskForm';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import ErrorMessage from '@/components/ui/ErrorMessage';

export default function TaskDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const [task, setTask] = useState<Todo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const taskId = params.id as string;

  useEffect(() => {
    const fetchTask = async () => {
      try {
        setError(null);
        const data = await todoApi.getById(taskId);
        setTask(data);
      } catch (err: unknown) {
        const error = err as { response?: { status?: number; data?: { detail?: string } } };
        if (error.response?.status === 404) {
          setError('Task not found');
        } else {
          setError(error.response?.data?.detail || 'Failed to load task');
        }
      } finally {
        setIsLoading(false);
      }
    };

    if (taskId) {
      fetchTask();
    }
  }, [taskId]);

  const handleSubmit = async (data: TodoUpdate) => {
    await todoApi.update(taskId, data as TodoUpdate);
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await todoApi.delete(taskId);
      router.push('/tasks');
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || 'Failed to delete task');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-12">
        <ErrorMessage message={error} onRetry={() => router.push('/tasks')} />
      </div>
    );
  }

  if (!task || !user) {
    return null;
  }

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Edit Task</h1>
          <p className="mt-1 text-sm text-gray-600">
            Update your task details
          </p>
        </div>
        <button
          onClick={handleDelete}
          className="rounded-md border border-red-300 bg-white px-4 py-2 text-sm font-medium text-red-600 shadow-sm hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          Delete Task
        </button>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <TaskForm task={task} userId={user.id} onSubmit={handleSubmit} isEdit />
      </div>
    </div>
  );
}

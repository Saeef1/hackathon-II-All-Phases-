'use client';

import { useAuth } from '@/lib/auth-context';
import { todoApi } from '@/lib/api-client';
import { TodoCreate, TodoUpdate } from '@/lib/types';
import TaskForm from '@/components/tasks/TaskForm';

export default function NewTaskPage() {
  const { user } = useAuth();

  const handleSubmit = async (data: TodoCreate | TodoUpdate) => {
    await todoApi.create(data as TodoCreate);
  };

  if (!user) {
    return null;
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Create New Task</h1>
        <p className="mt-1 text-sm text-gray-600">
          Add a new task to your list
        </p>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <TaskForm userId={user.id} onSubmit={handleSubmit} />
      </div>
    </div>
  );
}

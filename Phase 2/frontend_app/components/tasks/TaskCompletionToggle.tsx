'use client';

interface TaskCompletionToggleProps {
  isCompleted: boolean;
  onToggle: () => void;
  disabled?: boolean;
}

export default function TaskCompletionToggle({
  isCompleted,
  onToggle,
  disabled = false,
}: TaskCompletionToggleProps) {
  return (
    <button
      onClick={onToggle}
      disabled={disabled}
      className={`flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full border-2 transition-colors ${
        isCompleted
          ? 'border-green-500 bg-green-500 text-white'
          : 'border-gray-300 hover:border-green-500'
      } ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}
      aria-label={isCompleted ? 'Mark as incomplete' : 'Mark as complete'}
    >
      {isCompleted && (
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
        </svg>
      )}
    </button>
  );
}

/**
 * Unit tests for task search functionality
 */

// Import the function to test (in a real setup, this would be properly imported)
function filterTasksByTitle(tasks, searchTerm) {
  if (!searchTerm || !searchTerm.trim()) {
    return tasks;
  }

  const term = searchTerm.toLowerCase().trim();
  return tasks.filter(task => task.title.toLowerCase().includes(term));
}

describe('filterTasksByTitle', () => {
  const mockTasks = [
    { id: 1, title: 'Math Homework', status: 'Pending' },
    { id: 2, title: 'Science Project', status: 'In Progress' },
    { id: 3, title: 'History Essay', status: 'Completed' },
    { id: 4, title: 'Math Quiz Preparation', status: 'Pending' },
    { id: 5, title: 'Art Assignment', status: 'Pending' }
  ];

  test('returns all tasks when search term is empty', () => {
    const result = filterTasksByTitle(mockTasks, '');
    expect(result).toEqual(mockTasks);
    expect(result.length).toBe(5);
  });

  test('returns all tasks when search term is null', () => {
    const result = filterTasksByTitle(mockTasks, null);
    expect(result).toEqual(mockTasks);
  });

  test('returns all tasks when search term is undefined', () => {
    const result = filterTasksByTitle(mockTasks, undefined);
    expect(result).toEqual(mockTasks);
  });

  test('returns all tasks when search term is only whitespace', () => {
    const result = filterTasksByTitle(mockTasks, '   ');
    expect(result).toEqual(mockTasks);
  });

  test('filters tasks by exact title match', () => {
    const result = filterTasksByTitle(mockTasks, 'Math Homework');
    expect(result.length).toBe(1);
    expect(result[0].title).toBe('Math Homework');
  });

  test('filters tasks by partial title match', () => {
    const result = filterTasksByTitle(mockTasks, 'Math');
    expect(result.length).toBe(2);
    expect(result.map(t => t.title)).toEqual(['Math Homework', 'Math Quiz Preparation']);
  });

  test('filters tasks case-insensitively', () => {
    const result = filterTasksByTitle(mockTasks, 'math');
    expect(result.length).toBe(2);
    expect(result.map(t => t.title)).toEqual(['Math Homework', 'Math Quiz Preparation']);
  });

  test('filters tasks with mixed case search term', () => {
    const result = filterTasksByTitle(mockTasks, 'ScIeNcE');
    expect(result.length).toBe(1);
    expect(result[0].title).toBe('Science Project');
  });

  test('returns empty array when no tasks match', () => {
    const result = filterTasksByTitle(mockTasks, 'Nonexistent Task');
    expect(result).toEqual([]);
  });

  test('handles empty task array', () => {
    const result = filterTasksByTitle([], 'Math');
    expect(result).toEqual([]);
  });

  test('trims whitespace from search term', () => {
    const result = filterTasksByTitle(mockTasks, '  Math  ');
    expect(result.length).toBe(2);
    expect(result.map(t => t.title)).toEqual(['Math Homework', 'Math Quiz Preparation']);
  });

  test('matches substring anywhere in title', () => {
    const result = filterTasksByTitle(mockTasks, 'Project');
    expect(result.length).toBe(1);
    expect(result[0].title).toBe('Science Project');
  });

  test('does not match when search term is longer than title', () => {
    const result = filterTasksByTitle(mockTasks, 'Math Homework Assignment');
    expect(result).toEqual([]);
  });
});
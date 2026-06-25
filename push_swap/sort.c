/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 18:20:51 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/23 18:20:54 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	sort_three(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	top;
	int	mid;
	int	bot;

	top = (*a)->value;
	mid = (*a)->next->value;
	bot = (*a)->next->next->value;
	if (top > mid && mid < bot && top < bot)
		exec_swap(a, b, 'a', bnch);
	else if (top > mid && mid > bot)
		(exec_swap(a, b, 'a', bnch), exec_rev_rotate(a, b, 'a', bnch));
	else if (top > mid && top > bot && mid < bot)
		exec_rotate(a, b, 'a', bnch);
	else if (top < mid && mid > bot && top < bot)
		(exec_swap(a, b, 'a', bnch), exec_rotate(a, b, 'a', bnch));
	else if (top < mid && mid > bot && top > bot)
		exec_rev_rotate(a, b, 'a', bnch);
}

static void	insert_one(t_stack **a, t_stack **b, t_bench *bnch, int size)
{
	int	pos;
	int	val;

	val = (*b)->value;
	pos = 0;
	while (pos < size && (*a)->value < val)
	{
		exec_rotate(a, b, 'a', bnch);
		pos++;
	}
	exec_push(a, b, 'a', bnch);
	while (pos-- > 0)
		exec_rev_rotate(a, b, 'a', bnch);
}

void	strategy_simple(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	size;

	size = stack_size(*a);
	if (size == 2 && (*a)->value > (*a)->next->value)
		return (exec_swap(a, b, 'a', bnch));
	if (size == 3 && !is_sorted(*a))
		return (sort_three(a, b, bnch));
	while (stack_size(*a) > 3)
		exec_push(b, a, 'b', bnch);
	sort_three(a, b, bnch);
	while (*b)
		insert_one(a, b, bnch, stack_size(*a));
}

void	strategy_medium(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	size;
	int	chunk_size;
	int	current_chunk;

	size = stack_size(*a);
	chunk_size = size / 5;
	if (chunk_size == 0)
		chunk_size = 1;
	current_chunk = chunk_size;
	while (*a)
	{
		if ((*a)->index <= current_chunk)
		{
			exec_push(b, a, 'b', bnch);
			if (*b && (*b)->next
				&& (*b)->index < (current_chunk - (chunk_size / 2)))
				exec_rotate(a, b, 'b', bnch);
		}
		else
			exec_rotate(a, b, 'a', bnch);
		if (stack_size(*b) >= current_chunk && current_chunk < size)
			current_chunk += chunk_size;
	}
	push_b_to_a(a, b, bnch);
}

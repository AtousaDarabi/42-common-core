/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strategy_simple.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 21:07:38 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:08:14 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	find_min_value(t_stack *stack)
{
	int	min;

	min = stack->value;
	while (stack)
	{
		if (stack->value < min)
			min = stack->value;
		stack = stack->next;
	}
	return (min);
}

void	sort_three(t_stack **a, t_bench *b)
{
	int	first;
	int	second;
	int	third;

	first = (*a)->value;
	second = (*a)->next->value;
	third = (*a)->next->next->value;
	if (first > second && second < third && first < third)
		sa(a, b);
	else if (first > second && second > third)
	{
		sa(a, b);
		rra(a, b);
	}
	else if (first > second && second < third && first > third)
		ra(a, b);
	else if (first < second && second > third && first < third)
	{
		sa(a, b);
		ra(a, b);
	}
	else if (first < second && second > third && first > third)
		rra(a, b);
}

void	sort_five(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	min;

	while (bnch->total_ops < 50 && (*a)->next && (*a)->next->next && (*a)->next->next->next)
	{
		min = find_min_value(*a);
		while ((*a)->value != min)
		{
			// Write the operation to move the minimum value to the top of stack A
			rra(a, bnch); 
		}
		pb(a, b, bnch);
	}
	sort_three(a, bnch);
	while (*b)
		pa(a, b, bnch);
}

void	strategy_simple(t_stack **a, t_stack **b, t_bench *bnch, int size)
{
	if (size <= 1)
		return ;
	if (size == 2)
	{
		if ((*a)->value > (*a)->next->value)
			sa(a, bnch);
	}
	else if (size == 3)
		sort_three(a, bnch);
	else if (size <= 5)
		sort_five(a, b, bnch);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operations_two.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 21:04:25 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:04:27 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	ra(t_stack **a, t_bench *b)
{
	t_stack	*first;
	t_stack	*last;

	if (!a || !*a || !(*a)->next)
		return ;
	first = *a;
	*a = first->next;
	last = *a;
	while (last->next)
		last = last->next;
	last->next = first;
	first->next = NULL;
	if (b && b->active)
		b->ra++;
	else
		write(1, "ra\n", 3);
	if (b)
		b->total_ops++;
}

void	rb(t_stack **b_stk, t_bench *b)
{
	t_stack	*first;
	t_stack	*last;

	if (!b_stk || !*b_stk || !(*b_stk)->next)
		return ;
	first = *b_stk;
	*b_stk = first->next;
	last = *b_stk;
	while (last->next)
		last = last->next;
	last->next = first;
	first->next = NULL;
	if (b && b->active)
		b->rb++;
	else
		write(1, "rb\n", 3);
	if (b)
		b->total_ops++;
}

void	rr(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	prev_active;

	if (bnch)
	{
		prev_active = bnch->active;
		bnch->active = 1;
	}
	ra(a, bnch);
	rb(b, bnch);
	if (bnch)
	{
		bnch->active = prev_active;
		if (bnch->active)
			bnch->rr++;
		else
			write(1, "rr\n", 3);
		bnch->total_ops--;
	}
	else
		write(1, "rr\n", 3);
}

void	rra(t_stack **a, t_bench *b)
{
	t_stack	*last;
	t_stack	*prev;

	if (!a || !*a || !(*a)->next)
		return ;
	prev = NULL;
	last = *a;
	while (last->next)
	{
		prev = last;
		last = last->next;
	}
	prev->next = NULL;
	last->next = *a;
	*a = last;
	if (b && b->active)
		b->rra++;
	else
		write(1, "rra\n", 3);
	if (b)
		b->total_ops++;
}

void	rrb(t_stack **b_stk, t_bench *b)
{
	t_stack	*last;
	t_stack	*prev;

	if (!b_stk || !*b_stk || !(*b_stk)->next)
		return ;
	prev = NULL;
	last = *b_stk;
	while (last->next)
	{
		prev = last;
		last = last->next;
	}
	prev->next = NULL;
	last->next = *b_stk;
	*b_stk = last;
	if (b && b->active)
		b->rrb++;
	else
		write(1, "rrb\n", 3);
	if (b)
		b->total_ops++;
}

void	rrr(t_stack **a, t_stack **b, t_bench *bnch)
{
	int	prev_active;

	if (bnch)
	{
		prev_active = bnch->active;
		bnch->active = 1;
	}
	rra(a, bnch);
	rrb(b, bnch);
	if (bnch)
	{
		bnch->active = prev_active;
		if (bnch->active)
			bnch->rrr++;
		else
			write(1, "rrr\n", 3);
		bnch->total_ops--;
	}
	else
		write(1, "rrr\n", 3);
}

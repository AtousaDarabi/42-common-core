/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   instructions.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 18:13:16 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/23 18:13:19 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ft_printf(const char *format, ...);

void	exec_swap(t_stack **a, t_stack **b, char type, t_bench *bnch)
{
	if (type == 'a')
	{
		swap(a);
		bnch->sa++;
		ft_putstr_fd("sa\n", 1);
	}
	else if (type == 'b')
	{
		swap(b);
		bnch->sb++;
		ft_putstr_fd("sb\n", 1);
	}
	else if (type == 's')
	{
		swap(a);
		swap(b);
		bnch->ss++;
		ft_putstr_fd("ss\n", 1);
	}
	bnch->total_ops++;
}

void	exec_push(t_stack **dest, t_stack **src, char type, t_bench *bnch)
{
	push(dest, src);
	if (type == 'a')
	{
		bnch->pa++;
		ft_putstr_fd("pa\n", 1);
	}
	else if (type == 'b')
	{
		bnch->pb++;
		ft_putstr_fd("pb\n", 1);
	}
	bnch->total_ops++;
}

void	exec_rotate(t_stack **a, t_stack **b, char type, t_bench *bnch)
{
	if (type == 'a')
	{
		rotate(a);
		bnch->ra++;
		ft_putstr_fd("ra\n", 1);
	}
	else if (type == 'b')
	{
		rotate(b);
		bnch->rb++;
		ft_putstr_fd("rb\n", 1);
	}
	else if (type == 'r')
	{
		rotate(a);
		rotate(b);
		bnch->rr++;
		ft_putstr_fd("rr\n", 1);
	}
	bnch->total_ops++;
}

void	exec_rev_rotate(t_stack **a, t_stack **b, char type, t_bench *bnch)
{
	if (type == 'a')
	{
		reverse_rotate(a);
		bnch->rra++;
		ft_putstr_fd("rra\n", 1);
	}
	else if (type == 'b')
	{
		reverse_rotate(b);
		bnch->rrb++;
		ft_putstr_fd("rrb\n", 1);
	}
	else if (type == 'r')
	{
		reverse_rotate(a);
		reverse_rotate(b);
		bnch->rrr++;
		ft_putstr_fd("rrr\n", 1);
	}
	bnch->total_ops++;
}

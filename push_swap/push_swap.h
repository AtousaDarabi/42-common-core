/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 17:46:15 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:12:34 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H
#include <unistd.h>

typedef struct s_stack
{
	int				value;
	int				index;
	struct s_stack	*next;
}	t_stack;

typedef struct s_bench
{
	int	active;
	int	total_ops;
	int	sa;
	int	sb;
	int	ss;
	int	pa;
	int	pb;
	int	ra;
	int	rb;
	int	rr;
	int	rra;
	int	rrb;
	int	rrr;
}	t_bench;

void	sa(t_stack **a, t_bench *b);
void	sb(t_stack **a, t_bench *b);
void	ss(t_stack **a, t_stack **b, t_bench *bnch);
void	pa(t_stack **a, t_stack **b, t_bench *bnch);
void	pb(t_stack **a, t_stack **b, t_bench *bnch);
void	ra(t_stack **a, t_bench *b);
void	rb(t_stack **a, t_bench *b);
void	rr(t_stack **a, t_stack **b, t_bench *bnch);
void	rra(t_stack **a, t_bench *b);
void	rrb(t_stack **a, t_bench *b);
void	rrr(t_stack **a, t_stack **b, t_bench *bnch);
double	compute_disorder(int *arr, int size);
int		*parse_arguments(int argc, char **argv, t_stack **a, int *size);
void	print_error_and_exit(t_stack **a, int *arr);
void	strategy_medium(t_stack **a, t_stack **b, t_bench *bnch, int size);
void	strategy_complex(t_stack **a, t_stack **b, t_bench *bnch, int size);
void	strategy_adaptive(t_stack **a, t_stack **b, t_bench *bnch, int size);

#endif

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 18:07:53 by jukohler          #+#    #+#             */
/*   Updated: 2026/06/26 11:29:28 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>
# include "libft.h"

# define MODE_SIMPLE	1
# define MODE_MEDIUM	2
# define MODE_COMPLEX	3
# define MODE_ADAPTIVE	4

typedef struct s_stack
{
	int				value;
	int				index;
	struct s_stack	*next;
}	t_stack;

typedef struct s_bench
{
	int		active;
	int		total_ops;
	int		sa;
	int		sb;
	int		ss;
	int		pa;
	int		pb;
	int		ra;
	int		rb;
	int		rr;
	int		rra;
	int		rrb;
	int		rrr;
	double	disorder;
}	t_bench;

int		ft_printf(const char *format, ...);
void	init_program(char **argv, t_stack **stack_a);

int		stack_size(t_stack *stack);
void	stack_add_back(t_stack **stack, t_stack *new_node);
void	free_stack(t_stack **stack);
int		is_sorted(t_stack *stack);
double	compute_disorder(t_stack *stack);

void	swap(t_stack **stack);
void	push(t_stack **dest, t_stack **src);
void	rotate(t_stack **stack);
void	reverse_rotate(t_stack **stack);
void	normalize_indices(t_stack *stack);

void	exec_swap(t_stack **a, t_stack **b, char type, t_bench *bnch);
void	exec_push(t_stack **dest, t_stack **src, char type, t_bench *bnch);
void	exec_rotate(t_stack **a, t_stack **b, char type, t_bench *bnch);
void	exec_rev_rotate(t_stack **a, t_stack **b, char type, t_bench *bnch);
void	print_bench_results(t_bench *b);

void	push_b_to_a(t_stack **a, t_stack **b, t_bench *bnch);
void	strategy_simple(t_stack **a, t_stack **b, t_bench *bnch);
void	strategy_medium(t_stack **a, t_stack **b, t_bench *bnch);
void	strategy_complex(t_stack **a, t_stack **b, t_bench *bnch);
void	execute_strategy(t_stack **a, t_stack **b, t_bench *bnch, int mode);
int		check_flags(char *arg, t_bench *b, int *mode);

#endif

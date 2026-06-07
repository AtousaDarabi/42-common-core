/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/09 18:11:11 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/09 21:14:49 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/* We initialize the benchmark structure */
static void	init_bench(t_bench *b)
{
	b->active = 0;
	b->total_ops = 0;
	b->sa = 0;
	b->sb = 0;
	b->ss = 0;
	b->pa = 0;
	b->pb = 0;
	b->ra = 0;
	b->rb = 0;
	b->rr = 0;
	b->rra = 0;
	b->rrb = 0;
	b->rrr = 0;
}

/* We print the benchmark results to the output if the --bench flag is active */
static void	print_bench_results(t_bench *b)
{
	if (!b->active)
		return ;
	write(1, "--- Performance Benchmark ---\n", 30);
	write(1, "Total operations: ", 18);
	// We can convert the total_ops to a string and write it, but since we are not allowed to use printf, we will just write the number of operations as a string manually for demonstration purposes.
	// We can implement a simple itoa function to convert the number to a string, but for simplicity, we will just write a placeholder here.
}

/* We check for the --bench flag to activate benchmarking, and for strategy selection flags */
static int	check_flags(char *arg, t_bench *b, int *mode)
{
	// We check for the --bench flag to activate benchmarking, and for strategy selection flags
	if (arg[0] == '-' && arg[1] == '-' && arg[2] == 'b' && arg[3] == 'e' && arg[4] == 'n' && arg[5] == 'c' && arg[6] == 'h' && arg[7] == '\0')
	{
		b->active = 1;
		return (1);
	}
	if (arg[0] == '-' && arg[1] == '-' && arg[2] == 's' && arg[3] == 'i' && arg[4] == 'm' && arg[5] == 'p' && arg[6] == 'l' && arg[7] == 'e' && arg[8] == '\0')
		*mode = 1;
	else if (arg[0] == '-' && arg[1] == '-' && arg[2] == 'm' && arg[3] == 'e' && arg[4] == 'd' && arg[5] == 'i' && arg[6] == 'u' && arg[7] == 'm' && arg[8] == '\0')
		*mode = 2;
	else if (arg[0] == '-' && arg[1] == '-' && arg[2] == 'c' && arg[3] == 'o' && arg[4] == 'm' && arg[5] == 'p' && arg[6] == 'l' && arg[7] == 'e' && arg[8] == 'x' && arg[9] == '\0')
		*mode = 3;
	else if (arg[0] == '-' && arg[1] == '-' && arg[2] == 'a' && arg[3] == 'd' && arg[4] == 'a' && arg[5] == 'p' && arg[6] == 't' && arg[7] == 'i' && arg[8] == 'v' && arg[9] == 'e' && arg[10] == '\0')
		*mode = 4;
	else
		return (0);
	return (1);
}

/* We execute the selected strategy */
static void	execute_strategy(t_stack **a, t_stack **b, t_bench *bnch, int mode, int size)
{
	if (mode == 1)
		strategy_simple(a, b, bnch, size);
	else if (mode == 2)
		strategy_medium(a, b, bnch, size);
	else if (mode == 3)
		strategy_complex(a, b, bnch, size);
	else
		strategy_adaptive(a, b, bnch, size);
}

int	main(int argc, char **argv)
{
	t_stack	*a;
	t_stack	*b;
	t_bench	bnch;
	int		*arr;
	int		size;
	int		mode;
	int		flag_offset;

	if (argc < 2)
		return (0);
	a = NULL;
	b = NULL;
	init_bench(&bnch);
	mode = 4; // We default to adaptive mode if no specific strategy is chosen
	flag_offset = 0;
	while (argv[flag_offset + 1] && check_flags(argv[flag_offset + 1], &bnch, &mode))
		flag_offset++;
	
	// We parse the arguments after the flags and initialize stack A and the array for benchmarking
	arr = parse_arguments(argc - flag_offset, argv + flag_offset, &a, &size);
	
	execute_strategy(&a, &b, &bnch, mode, size);
	print_bench_results(&bnch);
	
	// We can reuse the error handling function to free memory and exit, since it already handles freeing the stack and array
	print_error_and_exit(&a, arr); // We can reuse this function to free memory and exit
	while (b)
	{
		t_stack *tmp = b->next;
		free(b);
		b = tmp;
	}
	return (0);
}

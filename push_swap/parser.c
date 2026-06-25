/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/24 16:53:31 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/24 16:53:34 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	has_duplicate(t_stack *stack, int num)
{
	while (stack && stack->value != num)
		stack = stack->next;
	return (stack != NULL);
}

static void	handle_parse_error(t_stack **stack)
{
	free_stack(stack);
	ft_putstr_fd("Error\n", 2);
	exit(1);
}

static void	parse_token(char *token, t_stack **stack_a)
{
	t_stack	*new;
	int		val;
	int		error;

	error = 0;
	val = ft_atoi(token, &error);
	if (error || has_duplicate(*stack_a, val))
		handle_parse_error(stack_a);
	new = malloc(sizeof(t_stack));
	if (!new)
		handle_parse_error(stack_a);
	new->value = val;
	new->index = -1;
	new->next = NULL;
	stack_add_back(stack_a, new);
}

static void	parse_string(char *str, t_stack **stack_a)
{
	char	token[32];
	int		i;

	while (*str)
	{
		while (*str == ' ')
			str++;
		if (!*str)
			break ;
		i = 0;
		while (*str && *str != ' ')
			token[i++] = *str++;
		token[i] = '\0';
		if (i > 0)
			parse_token(token, stack_a);
	}
}

void	init_program(char **argv, t_stack **stack_a)
{
	while (*argv)
	{
		if ((*argv)[0] != '\0')
			parse_string(*argv, stack_a);
		argv++;
	}
}

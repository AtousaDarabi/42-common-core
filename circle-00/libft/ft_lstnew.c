/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 13:17:07 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstnew(void *content)
{
	t_list	*new_node;

	new_node = (t_list *)malloc(sizeof (t_list));
	if (!new_node)
		return (NULL);
	new_node->content = content;
	new_node->next = NULL;
	return (new_node);
}

// int	main(void)
// {
// 	t_list	*node;
// 	char	*content;

// 	content = "Hello, 42!";
// 	node = ft_lstnew(content);
// 	if (!node)
// 	{
// 		printf("Malloc failed!\n");
// 		return (1);
// 	}
// 	printf("Node Content: %s\n", (char *)node->content);
// 	if (node->next == NULL)
// 		printf("Next pointer is NULL (Correct)\n");
// 	else
// 		printf("Next pointer is NOT NULL (Error)\n");
// 	free(node);
// 	return (0);
// }

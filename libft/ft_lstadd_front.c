/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_front.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 13:38:41 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_front(t_list **lst, t_list *new)
{
	if (!lst || !new)
		return ;
	new->next = *lst;
	*lst = new;
}

// int	main(void)
// {
// 	t_list	*head;
// 	t_list	*node_a;
// 	t_list	*node_b;

// 	head = NULL;
// 	node_a = ft_lstnew("I was created first.");
// 	ft_lstadd_front(&head, node_a);
// 	node_b = ft_lstnew("I was created second, but I'm at the front!");
// 	ft_lstadd_front(&head, node_b);
// 	printf("First node in list: %s\n", (char *)head->content);
// 	if (head->next)
// 		printf("Second node in list: %s\n", (char *)head->next->content);
// 	free(node_b);
// 	free(node_a);
// 	return (0);
// }

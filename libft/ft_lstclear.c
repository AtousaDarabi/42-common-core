/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 14:44:49 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/07 00:53:33 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstclear(t_list **lst, void (*del)(void *))
{
	t_list	*temp;

	if (!lst || !del || !*lst)
		return ;
	while (*lst)
	{
		temp = (*lst)->next;
		ft_lstdelone(*lst, del);
		*lst = temp;
	}
	*lst = NULL;
}

// void	del_content(void *content)
// {
// 	free(content);
// }

// int	main(void)
// {
// 	t_list	*head;

// 	head = NULL;
// 	ft_lstadd_back(&head, ft_lstnew(ft_strdup("Node 1")));
// 	ft_lstadd_back(&head, ft_lstnew(ft_strdup("Node 2")));
// 	ft_lstadd_back(&head, ft_lstnew(ft_strdup("Node 3")));
// 	ft_lstclear(&head, del_content);
// 	if (head == NULL)
// 		printf("List cleared and head set to NULL.\n");
// 	return (0);
// }
